import sys
#sys.path.append('/home/shivam/Downloads/lib/python3.6/site-packages')
sys.path.append('/home/shivam/Downloads/face-recognition/lib/python3.6/site-packages')
import random
import cv2
import serial
from serial import Serial
import face_recognition
import pickle
import glob
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
import  pyshine as ps
import numpy as np
import json
import webbrowser
import time
import spotipy
import wikipedia
from time import strftime
import socket


HTML="""
<html>
<head>
<title>PyShine Live Streaming</title>
</head>

<body>
<center>
<center><img src="stream.mjpg" width='640' height='480' autoplay playsinline></center>
</body>
</html>
"""
# Building the AI
class ChatBot():
    def __init__(self, name):
        print("----- Starting up", name, "-----")
        self.name = name
    def speech_to_text(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as mic:
            os.system("mpg123 " + "listening.wav")
            print("Listening...")
            recognizer.adjust_for_ambient_noise(mic)
            audio = recognizer.listen(mic)
            self.text="ERROR"
        try:
            self.text = recognizer.recognize_google(audio)
            print("Me  --> ", self.text)
        except:
            print("Me  -->  ERROR")
        return self.text
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
        return text
    def wake_up(self, text):
        return True if self.name in text.lower() else False
    @staticmethod
    def action_time():
        return datetime.datetime.now().time().strftime('%H:%M')
    
def feed():    
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    StreamProps = ps.StreamProps
    StreamProps.set_Page(StreamProps,HTML)
    address = (s.getsockname()[0],9000) # Enter your IP address 
    StreamProps.set_Mode(StreamProps,'cv2')
    capture = cv2.VideoCapture(0)
    capture.set(cv2.CAP_PROP_BUFFERSIZE,4)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH,320)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT,240)       
    capture.set(cv2.CAP_PROP_FPS,30)
    StreamProps.set_Capture(StreamProps,capture)
    StreamProps.set_Quality(StreamProps,90)
    server = ps.Streamer(address,StreamProps)
    print('Server started at','http://'+address[0]+':'+str(address[1]))
    server.serve_forever()
    sleep(300)
    capture.release()
    server.socket.close()
    
def embedding():
    res= "What is your name?"
    ai.text_to_speech(res)
    name=ai.speech_to_text()
    ref_id=random.randint(100,1000)

    try:
        f=open("ref_name.pkl","rb")

        ref_dictt=pickle.load(f)
        f.close()
    except:
        ref_dictt={}
        ref_dictt[ref_id]=name


    f=open("ref_name.pkl","wb")
    pickle.dump(ref_dictt,f)
    f.close()

    try:
        f=open("ref_embed.pkl","rb")

        embed_dictt=pickle.load(f)
        f.close()
    except:
        embed_dictt={}





    for i in range(5):
        key = cv2. waitKey(1)
        webcam = cv2.VideoCapture(0)
        while True:
	     
            check, frame = webcam.read()
            # print(check) #prints true as long as the webcam is running
            # print(frame) #prints matrix values of each framecd 
            cv2.imshow("Capturing", frame)
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = small_frame[:, :, ::-1]
		
            key = cv2.waitKey(1)
            face_locations = face_recognition.face_locations(rgb_small_frame)
            if face_locations != []:

				# filename="photo.jpg"
				# cv2.imwrite(filename=filename, img=frame)
				# image = face_recognition.load_image_file(filename)
				# image = Image.fromarray(frame)
				# image = image.convert('RGB')
                face_encoding = face_recognition.face_encodings(frame)[0]
                if ref_id in embed_dictt:
                    embed_dictt[ref_id]+=[face_encoding]
                else:
                    embed_dictt[ref_id]=[face_encoding]
                webcam.release()
				# img_new = cv2.imread('saved_img.jpg', cv2.IMREAD_GRAYSCALE)
				# img_new = cv2.imshow("Captured Image", img_new)
                cv2.waitKey(1)
                cv2.destroyAllWindows()     
                break
		
    f=open("ref_embed.pkl","wb")
    pickle.dump(embed_dictt,f)
    f.close()
    
def recognise():
    f=open("ref_name.pkl","rb")
    ref_dictt=pickle.load(f)         #ref_dict=ref vs name
    f.close()

    f=open("ref_embed.pkl","rb")
    embed_dictt=pickle.load(f)      #embed_dict- ref  vs embedding 
    f.close()

    ############################################################################  encodings and ref_ids 
    known_face_encodings = []  #encodingd of faces
    known_face_names = []	   #ref_id of faces



    for ref_id , embed_list in embed_dictt.items():
        for embed in embed_list:
            known_face_encodings +=[embed]
            known_face_names += [ref_id]
                                                    


    #############################################################frame capturing from camera and face recognition
    video_capture = cv2.VideoCapture(0)
    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    while True  :
        
        ret, frame = video_capture.read()

        
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        
        rgb_small_frame = small_frame[:, :, ::-1]

        
        if process_this_frame:
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                    video_capture.release()
                    cv2.destroyAllWindows()
                face_names.append(name)
                n=ref_dictt[name]
                return n
    
def music_player():
    res="What song do you want me to play?"
    ai.text_to_speech(res)
    song=ai.speech_to_text()
    if song=="baby":
        os.system("mpg123 " + "baby.mp3")
    elif song=="once upon a time":
        os.system("mpg123 " + "once upon a time.mp3")
    elif song=="perfect":
        os.system("mpg123 " + "perfect.mp3")
    elif song=="love me like you do":
        os.system("mpg123 " + "love me like you do.mp3")
    elif song=="city of stars":
        os.system("mpg123 " + "city of stars.mp3")
    elif song=="feel me":
        os.system("mpg123 " + "feel me.mp3")
    elif song=="i am coming home":
        os.system("mpg123 " + "I am coming home.mp3")
    elif song=="let me down slowly":
        os.system("mpg123 " + "let me down slowly.mp3")
    elif song=="london boy":
        os.system("mpg123 " + "london boy.mp3")
    elif song=="neverland":
        os.system("mpg123 " + "neverland.mp3")
    elif song=="replay":
        os.system("mpg123 " + "replay.mp3")
    elif song=="shower":
        os.system("mpg123 " + "shower.mp3")
    elif song=="yummy":
        os.system("mpg123 " + "yummy.mp3")
    elif song=="the monster song":
        os.system("mpg123 " + "the monster song.mp3")
    elif song=="vikram":
        os.system("mpg123 " + "vikram.mp3")
    else:
        res="sorry!"
        ai.text_to_speech(res)
             
 
# Running the AI
if __name__ == "__main__":
    ai = ChatBot(name="Rio")
    res = "Hello I am Rio, what can I do for you?"
    ai.text_to_speech(res)
    ex=True
    while ex:
        ai.speech_to_text()
        if "what is" in ai.text or "who is" in ai.text or "which" in ai.text or "when" in ai.text:              
            client = wolframalpha.Client("KXU9TR-9EQ4J48YAJ")
            resu = client.query(ai.text)
            res=next(resu.results).text
        elif "define" in ai.text:              
             searching=ai.text.replace('define', '')
             res= wikipedia.summary(searching, 1)
        elif "see me" in ai.text:
            embedding()
            res="I caught you!"
        elif "what is your name" in ai.text or "who are you" in ai.text:
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
            name=recognise()
            actual= "Hello ", name
            string=''.join([str(item) for item in actual])
            res= string
        elif "time" in ai.text:
            res = ai.action_time()
        ## respond politely
        elif "music" in ai.text:
            music_player()
        elif "follow me" in ai.text:
            res= "following you!"
            ai.text_to_speech(res)
            ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
            ser.reset_input_buffer()
            ser.write(b"follow me")
            line = ser.readline().decode('utf-8').rstrip()
        elif "telepresence" in ai.text:
            res= "Telepresence mode activated"
            ai.text_to_speech(res)
            ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
            ser.reset_input_buffer()
            ser.write(b"telepresence")
            line = ser.readline().decode('utf-8').rstrip()
            feed()
            sleep(300)
        elif any(i in ai.text for i in ["thank","thanks"]):
            res = np.random.choice(["you're welcome!","anytime!","no problem!","cool!","I'm here if you need me!","mention not"])
        elif any(i in ai.text for i in ["exit","close"]):
            res = np.random.choice(["Tata","Have a good day","Bye","Goodbye","Hope to meet soon","peace out!"])
            ai.text_to_speech(res)
            ex=False
        else:   
            if ai.text=="ERROR":
                res="Sorry, come again?"
        ai.text_to_speech(res)
    print("----- Closing down Rio -----")
    sys.exit()


