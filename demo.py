import astro_base as ab
import spacy

nlp = spacy.load("en_core_web_sm")

agent = "jay"
bhudev = ab.astro


def preprocess(question):
    question = question.lower().strip()

    # 1. Exact Question Match
    for subject in bhudev:
        questions = [q.lower() for q in subject.get("questions", [])]

        if question in questions:
            answer = subject.get("answer", {})
            print(answer.get("overview"))
            print(answer.get("references"))
            return

    # 2. Keyword Match
    for subject in bhudev:
        keywords = [k.lower() for k in subject.get("keywords", [])]

        for keyword in keywords:
            if keyword in question:
                answer = subject.get("answer", {})
                print(answer.get("overview"))
                print(answer.get("references"))
                return
            
        for subject in bhudev:
            keywords_a = [k.lower() for k in subject.get("alternate_keywords", [])]

        for keyword in keywords_a:
            if keyword in question:
                answer = subject.get("answer", {})
                print(answer.get("overview"))
                print(answer.get("references"))
                return
    # 3. Token Match
    doc = nlp(question)

    for token in doc:
        for subject in bhudev:
            keywords = [k.lower() for k in subject.get("keywords", [])]

            for keyword in keywords:
                if token.text.lower() in keyword.split():
                    answer = subject.get("answer", {})
                    print(answer.get("overview"))
                    return

    print("Sorry, I don't have an answer to your question.")


while True:
    question = input("You : ")

    if question.lower() in ["bye", "exit"]:
        print("Good bye, see you again.")
        break

    preprocess(question)