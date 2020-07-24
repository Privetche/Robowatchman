import json
import time
import schedule
import pyttsx3

greetings = {'Ilya': 0, 'Evgeny': 0, 'unknown': 0, 'Sasha Grey': 0}
russian_names = {'Ilya': 'Илья', 'Evgeny': 'Женя', 'Sasha Grey': 'Саша Грей', 'unknown': 'анон'}
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # скорость речи
engine.setProperty('volume', 0.9)  # Громкость
phrases = {1: ['Ты еще кто такой?', float(0)]}


def new_day():
    for person in greetings:
        greetings[person] = 0


schedule.every().day.at("00:00").do(new_day)

while True:
    try:
        with open('visible_persons.txt', 'rb') as file:
            visible_persons = json.loads(file.read())
    except json.decoder.JSONDecodeError:
        visible_persons = {'Ilya': 0, 'Evgeny': 0, 'unknown': 0, 'Sasha Grey': 0}
        pass
    for person in visible_persons:
        if visible_persons[person] > 0.5 and greetings[person] == 0 and person != 'unknown':
            print('Приветствую, ' + russian_names[person])
            engine.say('Приветствую, ' + russian_names[person])
            engine.runAndWait()
            greetings[person] = 1
        elif person == 'unknown':
            if phrases[1][1] < 1:
                print(phrases[1][0])
                engine.say(phrases[1][0])
                phrases[1][1] = 60
    schedule.run_pending()
    for phrase in phrases:
        if phrases[phrase][1] >= 0.5:
            phrases[phrase][1] = phrases[phrase][1] - 0.5
    time.sleep(0.5)
