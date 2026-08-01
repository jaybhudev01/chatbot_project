import astro_base as ab
import re
import string
import random

nlp = None

def get_nlp():
    global nlp
    if nlp is None:
        try:
            import spacy
            nlp = spacy.load("en_core_web_sm")
        except Exception as e:
            class FallbackNLP:
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
            nlp = FallbackNLP()
    return nlp
agent = "jay: "
bhudev = ab.astro

def get_dynamic_astro_answer(answer_dict):
    options = []
    
    # 1. Text fields
    text_fields = {
        "overview": "Overview",
        "details": "Details",
        "career": "Career guidance",
        "education": "Education insights",
        "finance": "Financial prospects",
        "marriage": "Marriage analysis",
        "relationships": "Relationship guidance",
        "health": "Health and wellness",
        "spirituality": "Spiritual path",
        "personality": "Personality traits"
    }
    
    for field, label in text_fields.items():
        val = answer_dict.get(field)
        if val and isinstance(val, str):
            options.append(f"{label}: {val}")
            
    # 2. List fields
    list_fields = {
        "positive_effects": "Positive effects",
        "negative_effects": "Negative effects",
        "strengths": "Strengths",
        "weaknesses": "Weaknesses",
        "precautions": "Precautions",
        "remedies": "Remedies",
        "mantras": "Mantras",
        "charity": "Charity recommendations",
        "fasting": "Fasting guidelines"
    }
    
    for field, label in list_fields.items():
        val_list = answer_dict.get(field)
        if val_list and isinstance(val_list, list):
            for item in val_list:
                options.append(f"{label}: {item}")
                
    if not options:
        return "No detailed answer available."
        
    return random.choice(options)

def get_best_astro_answer(answer_dict, question):
    question_lower = question.lower()
    
    # Topic mapping based on question content
    mapping = {
        "marriage": ["marriage", "relationships"],
        "compatibility": ["marriage", "relationships"],
        "husband": ["marriage"],
        "wife": ["marriage"],
        "partner": ["relationships", "marriage"],
        
        "career": ["career"],
        "job": ["career"],
        "profession": ["career"],
        "work": ["career"],
        
        "money": ["finance"],
        "finance": ["finance"],
        "wealth": ["finance"],
        "rich": ["finance"],
        "financial": ["finance"],
        
        "study": ["education"],
        "education": ["education"],
        "learn": ["education"],
        "school": ["education"],
        "college": ["education"],
        "intellect": ["education"],
        
        "health": ["health"],
        "disease": ["health"],
        "illness": ["health"],
        "body": ["health"],
        
        "spirituality": ["spirituality"],
        "karma": ["spirituality", "overview"],
        "dharma": ["spirituality"],
        "moksha": ["spirituality"],
        
        "remedy": ["remedies", "charity", "fasting"],
        "remedies": ["remedies", "charity", "fasting"],
        "upaya": ["remedies", "charity", "fasting"],
        "charity": ["charity"],
        "fast": ["fasting"],
        "fasting": ["fasting"],
        
        "mantra": ["mantras"],
        "mantras": ["mantras"],
        
        "strength": ["strengths"],
        "strengths": ["strengths"],
        "weakness": ["weaknesses"],
        "weaknesses": ["weaknesses"],
        "limit": ["weaknesses"],
        "limitation": ["weaknesses"],
        
        "positive": ["positive_effects"],
        "benefit": ["positive_effects"],
        "negative": ["negative_effects"],
        "harm": ["negative_effects"],
        "fear": ["negative_effects"],
        
        "precaution": ["precautions"],
        "deity": ["deities"],
        "deities": ["deities"],
        "god": ["deities"],
        
        "differ": ["details"],
        "western": ["details"],
        "tropical": ["details"],
        "sidereal": ["details"],
        "history": ["details"],
        "scripture": ["details"],
        "book": ["details"],
        "planet": ["details"],
        "nine planets": ["details"],
        "navagraha": ["details"]
    }
    
    matched_keys = []
    for keyword, keys in mapping.items():
        if keyword in question_lower:
            matched_keys.extend(keys)
            
    valid_options = []
    for key in matched_keys:
        val = answer_dict.get(key)
        if val:
            if isinstance(val, list) and val:
                for item in val:
                    valid_options.append((key, item))
            elif isinstance(val, str) and val.strip():
                valid_options.append((key, val))
                
    if valid_options:
        chosen_key, chosen_val = random.choice(valid_options)
        label = chosen_key.replace("_", " ").title()
        return f"{label}: {chosen_val}"
        
    # If no specific keywords matched, default to overview or details
    options = []
    if answer_dict.get("overview"):
        options.append(f"Overview: {answer_dict.get('overview')}")
    if answer_dict.get("details"):
        options.append(f"Details: {answer_dict.get('details')}")
        
    if options:
        return random.choice(options)
        
    return get_dynamic_astro_answer(answer_dict)

def preprocess(question):
    # Normalize the question: lowercase, stripped, and without punctuation
    question_lower = question.lower().strip()
    question_clean = question_lower.translate(str.maketrans('', '', string.punctuation))

    # 1. Exact Question Match
    for subject in bhudev:
        questions = [q.lower().strip().translate(str.maketrans('', '', string.punctuation)) for q in subject.get("questions", [])]
        if question_clean in questions:
            print(agent + get_best_astro_answer(subject.get("answer", {}), question_clean))
            return

    # 2. Multi-word Keyword Match
    for subject in bhudev:
        keywords = [kw.lower().strip() for kw in subject.get("keywords", []) + subject.get("alternate_keywords", [])]
        for kw in keywords:
            if " " in kw and re.search(r'\b' + re.escape(kw) + r'\b', question_clean):
                print(agent + get_best_astro_answer(subject.get("answer", {}), question_clean))
                return

    # 3. Token / Single-word Keyword Match (NLP)
    doc = get_nlp()(question_clean)
    for token in doc:
        token_text = token.text.lower()
        for subject in bhudev:
            keywords = [kw.lower().strip() for kw in subject.get("keywords", []) + subject.get("alternate_keywords", [])]
            if token_text in keywords:
                print(agent + get_best_astro_answer(subject.get("answer", {}), question_clean))
                return

    print(agent + "Sorry, I don't have an answer to your question.")

if __name__ == '__main__':
    while True:
        question = input("You : ")
        if question.lower().strip() in ["bye", "exit"]:
            print(agent + "Good bye see you again.")
            break
        else:    
            preprocess(question)
       