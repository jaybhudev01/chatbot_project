import jully_panchang as jp

agent = "jay:"

data = jp.panchang()

while True:

    question = input("you: ").strip()

    if question.lower() in ["bye", "exit"]:
        print(agent, "Good bye, Tata")
        break

    if question in data:
        print(agent, data[question])
    else:
        print(agent, "I don't have data for that date yet. Try a date like 2026-07-29.")