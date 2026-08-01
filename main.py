import os
import re
import uuid
from datetime import datetime
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
import uvicorn

# Import the refactored chatbot functions
import chatbot

app = FastAPI(title="Skisha Chatbot Web API", version="1.0.0")

# Enable CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure the log directory exists
LOG_DIR = "log"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Memory storage for active chatbot sessions
# In-memory dictionary for session state
active_sessions = {}

# Regex patterns for validation (matching chatbot.py patterns)
EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
MOBILE_REGEX = r'^\+?[0-9]{10,12}$'

# Pydantic Schemas
class StartSessionRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(...)
    mobile: str = Field(...)

class ChatMessageRequest(BaseModel):
    session_id: str
    message: str

class EndSessionRequest(BaseModel):
    session_id: str



@app.post("/api/start")
async def start_session(req: StartSessionRequest):
    # Normalize and strip inputs
    name = req.name.strip()
    email = req.email.strip()
    mobile = req.mobile.strip()

    # Validate email
    if not re.match(EMAIL_REGEX, email):
        raise HTTPException(status_code=400, detail="Invalid email format. Please check your email.")

    # Validate mobile (allow optional leading + and 10 to 12 digits)
    if not re.match(MOBILE_REGEX, mobile):
        raise HTTPException(
            status_code=400, 
            detail="Invalid mobile number. It must be between 10 to 12 digits, optionally starting with '+'."
        )

    # Generate session ID
    session_id = str(uuid.uuid4())
    start_time = datetime.now() #current date and time

    # Generate log file path
    clean_name = re.sub(r'[^a-zA-Z0-9]', '_', name) #ankit_patel
    timestamp = start_time.strftime("%Y-%m-%d_%H-%M-%S") 
    log_filepath = os.path.join(LOG_DIR, f"{clean_name}_{timestamp}.txt")
    # log/ankit_patel_2026-07-2008:21:15.txt
    # Initialize log file
    try:
        with open(log_filepath, "w", encoding="utf-8") as f:
            f.write(f"Name: {name}\n")
            f.write(f"Email: {email}\n")
            f.write(f"Mobile: {mobile}\n")
            f.write("-" * 40 + "\n")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create session log: {str(e)}")

    # Save session details
    active_sessions[session_id] = {
        "name": name,
        "email": email,
        "mobile": mobile,
        "log_filepath": log_filepath,
        "start_time": start_time
    }

    return {
        "session_id": session_id,
        "name": name,
        "email": email,
        "mobile": mobile
    }

@app.post("/api/chat")
async def chat_message(request: ChatMessageRequest):
    session_id = request.session_id
    message = request.message

    if session_id not in active_sessions:
        raise HTTPException(status_code=404, detail="Session not found or has been expired.")

    session = active_sessions[session_id]
    log_filepath = session["log_filepath"]

    # Append user question to log
    try:
        with open(log_filepath, "a", encoding="utf-8") as f:
            f.write(f"You : {message}\n")
    except Exception as e:
        # Log error to console but don't crash request
        print(f"Error writing user msg to log: {e}")

    # Process response
    response_lines = []
    def custom_print(*args, **kwargs):
        line = " ".join(str(arg) for arg in args)
        response_lines.append(line)

    # Check for direct exit command
    message_lower = message.strip().lower()
    if message_lower in ["bye", "exit"]:
        bot_response = f"{chatbot.agent} Good bye see you again,"
        # Log response
        try:
            with open(log_filepath, "a", encoding="utf-8") as f:
                f.write(bot_response + "\n")
        except Exception as e:
            print(f"Error writing bot exit response to log: {e}")
        return {"response": bot_response}

    # Standard preprocessing (findout response using chatbot.py)
    chatbot.preprocess(message, print_func=custom_print)
    bot_response = "\n".join(response_lines)

    # Append response to log
    try:
        with open(log_filepath, "a", encoding="utf-8") as f:
            f.write(bot_response + "\n")
    except Exception as e:
        print(f"Error writing bot response to log: {e}")

    return {"response": bot_response}

@app.post("/api/end")
async def end_session(req: EndSessionRequest):
    session_id = req.session_id

    if session_id not in active_sessions:
        raise HTTPException(status_code=404, detail="Session not found or has expired.")

    session = active_sessions[session_id]
    name = session["name"]
    log_filepath = session["log_filepath"]
    start_time = session["start_time"]

    end_time = datetime.now() #store current time 
    duration = end_time - start_time #
    duration_str = f"{duration.seconds // 60} minutes, {duration.seconds % 60} seconds"

    # Append duration footer and close session log
    try:
        with open(log_filepath, "a", encoding="utf-8") as f:
            f.write("-" * 40 + "\n")
            f.write(f"Conversation duration: {duration_str}\n")
    except Exception as e:
        print(f"Error closing session log: {e}")

    # Trigger sending email
    email_sent = chatbot.send_chat_log_email(log_filepath, name)

    # Clean up session from memory
    del active_sessions[session_id]

    return {
        "status": "success",
        "email_sent": email_sent,
        "message": "Chat session ended successfully and logs have been emailed."
    }

# Mount static folder for serving static files (HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

#define route for root (home of website)
# //http://127.0.0.1:8000 
@app.get("/")
async def serve_index():
    return FileResponse("static/index.html")

if __name__ == '__main__':
    import sys
    
    # Interactive SMTP Setup if .env is not configured
    env_file = ".env"
    need_password = False
    
    if os.path.exists(env_file):
        try:
            with open(env_file, "r", encoding="utf-8") as f:
                content = f.read()
            if "YOUR_GMAIL_APP_PASSWORD" in content:
                need_password = True
        except Exception:
            need_password = True
    else:
        need_password = True
        
    if need_password:
        print("\n" + "*"*60)
        print("  GMAIL SMTP CONFIGURATION REQUIRED")
        print("  To receive chat logs at jaybhudev01@gmail.com,")
        print("  we need to configure your Gmail App Password.")
        print("*"*60 + "\n")
        try:
            # Use sys.stdin check to see if we can read input
            if sys.stdin and sys.stdin.isatty():
                choice = input("Would you like to enter your Gmail App Password now? (y/n): ").strip().lower()
                if choice == 'y':
                    app_pw = input("Please paste/type your 16-character App Password: ").strip()
                    if app_pw:
                        env_content = (
                            "# SMTP Email Configuration\n"
                            "SMTP_SERVER=smtp.gmail.com\n"
                            "SMTP_PORT=587\n"
                            "SMTP_USERNAME=jaybhudev01@gmail.com\n"
                            f"SMTP_PASSWORD={app_pw}\n"
                            "FROM_EMAIL=jaybhudev01@gmail.com\n"
                        )
                        with open(env_file, "w", encoding="utf-8") as f:
                            f.write(env_content)
                        print("[SUCCESS] App Password saved to .env file successfully!")
                        
                        os.environ["SMTP_SERVER"] = "smtp.gmail.com"
                        os.environ["SMTP_PORT"] = "587"
                        os.environ["SMTP_USERNAME"] = "jaybhudev01@gmail.com"
                        os.environ["SMTP_PASSWORD"] = app_pw
                        os.environ["FROM_EMAIL"] = "jaybhudev01@gmail.com"
                    else:
                        print("No password entered. Skipping SMTP setup.")
                else:
                    print("Skipping SMTP setup. You can configure it manually in the .env file later.")
            else:
                print("Non-interactive session detected. Skipping prompt.")
        except Exception as e:
            print(f"Skipping interactive setup: {e}")

    # Default host and port
    host = "127.0.0.1"
    port = 8000
    
    # Allow port to be specified as command line argument (e.g. python main.py 800)
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print(f"Invalid port number. Defaulting to {port}.")
            
    print("\n" + "="*50)
    print("  EasyLearn Academy Chatbot Server Starting...")
    print("  To access the chatbot, please open in your browser:")
    print(f"  --> http://{host}:{port}")
    print(f"  --> or http://localhost:{port}")
    print("="*50 + "\n")
    
    # Run the uvicorn development server
    uvicorn.run("main:app", host=host, port=port, reload=True)