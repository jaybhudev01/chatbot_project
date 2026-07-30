import knowledge_base as k
import spacy

agent = "siksha"
while True:
    question = input("you:")
    for item in k.greetings:
        if question == item.get('message'):
            print(agent,item.get('reply'))
    if question == "bye" or question == "exit":
        print("Good bye,see you again..")
        break
    