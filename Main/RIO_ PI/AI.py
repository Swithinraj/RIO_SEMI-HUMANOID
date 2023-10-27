# for speech-to-text
import speech_recognition as sr
import wolframalpha
# for text-to-speech
from gtts import gTTS
# for language model
import transformers
import re
import os
import time
import datetime
import numpy as np
import wikipedia
from time import strftime
# Building the AI
class ChatBot():
    def __init__(self, name):
        print("----- Starting up", name, "-----")
        self.name = name
    def speech_to_text(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as mic:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(mic)
            audio = recognizer.listen(mic)
            self.text="ERROR"
        try:
            self.text = recognizer.recognize_google(audio)
            print("Me  --> ", self.text)
        except:
            print("Me  -->  ERROR")
    @staticmethod
    def text_to_speech(text):
        print("Rio --> ", text)
        speaker = gTTS(text=text, lang="en", slow=False)
        speaker.save("res.mp3")
        statbuf = os.stat("res.mp3")
        mbytes = statbuf.st_size / 1024
        duration = mbytes / 200
        os.system("mpg123 " + "res.mp3")
        time.sleep(int(50*duration))
        os.remove("res.mp3")
    def wake_up(self, text):
        return True if self.name in text.lower() else False
    @staticmethod
    def action_time():
        return datetime.datetime.now().time().strftime('%H:%M')
# Running the AI
if __name__ == "__main__":
    ai = ChatBot(name="Rio")
    ex=True
    while ex:
        ai.speech_to_text()
        ## wake up
        if ai.wake_up(ai.text) is True:
            res = "Hello I am Rio, what can I do for you?"
        elif "what is" in ai.text or "who is" in ai.text or "which" in ai.text or "when" in ai.text:              
            client = wolframalpha.Client("KXU9TR-9EQ4J48YAJ")
            resu = client.query(ai.text)
            res=next(resu.results).text
        elif "define" in ai.text:              
             searching=ai.text.replace('define', '')
             res= wikipedia.summary(searching, 1)
        elif "see me" in ai.text:
            exec(open("embeddings.py").read())
            res="I caught you!"
        elif "your name" in ai.text:
            res="My name is Rio! I am your physical companion"
        elif 'hello' in ai.text:
            day_time = int(strftime('%H'))
            if day_time < 12:
                res='Hello! Good morning'
            elif 12 <= day_time < 18:
                res='Hello! Good afternoon'
            else:
                res='Hello! Good evening'    

        elif "recognise me" in ai.text:
            from recognition import name
            recognized=recognition.name
            res= "Oh! Hello", recognized
            break
        elif "time" in ai.text:
            res = ai.action_time()
        ## respond politely
        elif "follow me" in ai.text:
            res= "following you!"
            ai.text_to_speech(res)
            exec(open("CONNECTION.py").read())
        elif any(i in ai.text for i in ["thank","thanks"]):
            res = np.random.choice(["you're welcome!","anytime!","no problem!","cool!","I'm here if you need me!","mention not"])
        elif any(i in ai.text for i in ["exit","close"]):
            res = np.random.choice(["Tata","Have a good day","Bye","Goodbye","Hope to meet soon","peace out!"])
            ex=False
        else:   
            if ai.text=="ERROR":
                res="Sorry, come again?"
        ai.text_to_speech(res)
    print("----- Closing down Rio -----")
    sys.exit()

