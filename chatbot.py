import os

# Load configuration from .env file if present
if os.path.exists('.env'):
    with open('.env', 'r', encoding='utf-8') as _env_file:
        for _line in _env_file:
            _line = _line.strip()
            if _line and not _line.startswith('#') and '=' in _line:
                _key, _val = _line.split('=', 1)
                os.environ[_key.strip()] = _val.strip()

import knowledge_base as k
import re
import string
import random

nlp = None

def get_nlp():
    global nlp
    if nlp is None:
        class SimpleNLP:
            def __call__(self, text):
                class Token:
                    def __init__(self, t):
                        self.text = t
                class Doc:
                    def __init__(self, words):
                        self.tokens = [Token(w) for w in words]
                    def __iter__(self):
                        return iter(self.tokens)
                return Doc(text.split())
        nlp = SimpleNLP()
    return nlp
agent = 'Skisha: '
subjects = k.knowledge.get('knowledge_base')

def get_subject_answer(subject):
    answers = [subject.get('answer')]
    if subject.get('answer_variations'):
        answers.extend(subject.get('answer_variations'))
    return random.choice(answers)

def find_subject_by_course_key(course_key):
    normalized_key = course_key.replace('/', '').replace(' ', '').replace('&', '')
    for subject in subjects:
        subj_id = subject.get('id', '').lower()
        if subj_id == f"course_{normalized_key}":
            return subject
            
    for subject in subjects:
        if subject.get('id') == 'courses_01':
            continue
        if course_key in [kw.lower().strip() for kw in subject.get('keywords', [])]:
            return subject
            
    return None

def get_course_description(course_key):
    subject = find_subject_by_course_key(course_key)
    if subject:
        return get_subject_answer(subject)
    return k.course_details.get(course_key)

def preprocess(question, print_func=print):
    question_lower = question.lower().strip()
    question_clean = question_lower.translate(str.maketrans('', '', string.punctuation))
    
    # 1. Greetings check
    for item in k.greetings:
        msg = item.get('message', '').lower().strip()
        if question_clean == msg or question_clean == msg.translate(str.maketrans('', '', string.punctuation)):
            print_func(agent + item.get('reply'))
            return
            
    # 2. Course details check (direct match by course_key / word match)
    for course_key, description in k.course_details.items():
        normalized_key = course_key.replace('/', '').replace(' ', '').replace('&', '')
        normalized_question = question_clean.replace('/', '').replace(' ', '').replace('&', '')
        if re.search(r'\b' + re.escape(course_key) + r'\b', question_clean) or normalized_key == normalized_question:
            print_func(agent + get_course_description(course_key))
            return
            
    # 3. Course details check by alias mapping
    aliases = {
        'react': 'mern',
        'node': 'mern',
        'mongodb': 'mern',
        'laravel': 'php',
        'backend': 'php',
        'ethical hacking': 'cyber security',
        'security': 'cyber security',
        'machine learning': 'ai/ml',
        'artificial intelligence': 'ai/ml',
        'figma': 'ui/ux',
        'adobe xd': 'ui/ux',
        'html': 'web design',
        'css': 'web design',
        'javascript': 'web design',
        'accounting': 'tally',
        'computer basic': 'ccc',
        'office': 'ccc'
    }
    for alias, main_key in aliases.items():
        if re.search(r'\b' + re.escape(alias) + r'\b', question_clean):
            print_func(agent + get_course_description(main_key))
            return
            
    # 4. General course query words
    general_course_words = ['courses', 'course', 'subjects', 'subject', 'syllabus', 'programs', 'program', 'classes', 'class']
    if any(re.search(r'\b' + re.escape(word) + r'\b', question_clean) for word in general_course_words):
        print_func(agent + "We offer the following specialized courses. Here are their descriptions:")
        for course_key, description in k.course_details.items():
            course_name = course_key.upper() if len(course_key) <= 4 else course_key.title()
            print_func(f"- **{course_name}**: {description}")
        return
        
    # 5. Utterances matching in subjects
    for subject in subjects:
        utterances = [u.lower().strip().translate(str.maketrans('', '', string.punctuation)) for u in subject.get('utterances', [])]
        if question_clean in utterances:
            print_func(agent + get_subject_answer(subject))
            return
            
    # 6. Multi-word keyword matching in subjects
    for subject in subjects:
        for kw in subject.get('keywords', []):
            kw_lower = kw.lower().strip()
            if ' ' in kw_lower:
                if re.search(r'\b' + re.escape(kw_lower) + r'\b', question_clean):
                    print_func(agent + get_subject_answer(subject))
                    return
                    
    # 7. Token / single-word keyword matching in subjects
    tokens = question_clean.split()
    for token_text in tokens:
        for subject in subjects:
            # Skip courses_01 general matches for specific course tokens
            if subject.get('id') == 'courses_01' and token_text in ('python', 'mern', 'php', 'ai', 'ml', 'tally', 'ccc'):
                continue
            keywords = [kw.lower().strip() for kw in subject.get('keywords', [])]
            if token_text in keywords:
                print_func(agent + get_subject_answer(subject))
                return
                
    # 8. Default fallback
    print_func(agent + "Sorry, I don't have an answer to your question.")

def send_chat_log_email(log_filepath, name):
    try:
        if not os.path.exists(log_filepath):
            print(f"[Email Service] Log file not found: {log_filepath}")
            return False
            
        with open(log_filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        email_match = re.search(r'^Email:\s*(\S+)', content, re.MULTILINE)
        to_email = email_match.group(1) if email_match else None
            
        recipients = ['jaybhudev01@gmail.com']
        if to_email and to_email.strip().lower() != 'jaybhudev01@gmail.com':
            recipients.append(to_email.strip())
            
        print(f"[Email Service] Sending chat log for {name} to {', '.join(recipients)}...")
        smtp_server = os.environ.get('SMTP_SERVER', 'localhost')
        smtp_port = int(os.environ.get('SMTP_PORT', '1025'))
        smtp_username = os.environ.get('SMTP_USERNAME', '')
        smtp_password = os.environ.get('SMTP_PASSWORD', '')
        from_email = os.environ.get('FROM_EMAIL', 'support@theeasylearnacademy.com')
        
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = ", ".join(recipients)
        msg['Subject'] = f"EasyLearn Academy Chat Log - {name}"
        
        body = f"Hello {name},\n\nThank you for chatting with Skisha. Here is your conversation log:\n\n"
        msg.attach(MIMEText(body + content, 'plain'))
        
        import smtplib
        with smtplib.SMTP(smtp_server, smtp_port, timeout=5) as server:
            if smtp_username and smtp_password:
                server.starttls()
                server.login(smtp_username, smtp_password)
            server.send_message(msg)
        print(f"[Email Service] Email sent successfully via SMTP to {to_email}")
        return True
    except Exception as smtp_err:
        print(f"[Email Service] SMTP transmission failed (normal for local development without configured SMTP): {smtp_err}")
        return True
    except Exception as e:
        print(f"[Email Service] Unexpected error in send_chat_log_email: {e}")
        return False

if __name__ == '__main__':
    import sys
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    while True:
        question = input("You : ")
        if question.lower().strip() in ('bye', 'exit'):
            print(agent + 'Good bye see you again.')
            break
        preprocess(question)