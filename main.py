from concurrent.futures import thread
from datetime import time
from tkinter import *
# import spacy

from tkinter import Tk, Label, Frame, Scrollbar, RIGHT, Text, Entry, X, PhotoImage, Button, END

import pandas as pd
from chatterbot import ChatBot
from PIL import Image, ImageTk
from chatterbot.trainers import ListTrainer
import os
import pyttsx3
import speech_recognition
import threading
import pyaudio

# Initialize Text-to-Speech Engine
engine = pyttsx3.init()

# Get available voices
voices = engine.getProperty('voices')

# Select a female voice (varies by system)
for voice in voices:
    if "female" in voice.name.lower() or "zira" in voice.name.lower() or "samantha" in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break  # Stop after finding a female voice
# engine.setProperty(150)
# Function to Speak with Female Voice
def speak(text):
    engine.say(text)
    engine.runAndWait()
    engine.setProperty(120)
# from matplotlib.offsetbox import TextArea

# from ma import trainer
"""
# spacy.load("en_core_web_sm")
bot=ChatBot('Bot')
"""
bot=ChatBot('Mira')
trainer=ListTrainer(bot)

# for files in os.listdir('data/english/'):
    # data = open('data/english/'+files, 'r', encoding='utf-8').readlines()
    # trainer.train(data)r
# Training Data (Plant Disease Knowledge)
""""
training_data = [
    "What is Late Blight?",
    "Late Blight is a fungal disease affecting tomatoes and potatoes, caused by Phytophthora infestans.",
    "What are the symptoms of Late Blight?",
    "Dark lesions appear on leaves, and white mold forms on the undersides.",
    "How to prevent Late Blight?",
    "Use disease-resistant varieties, improve air circulation, and avoid overhead watering.",
    "How to treat Late Blight?",
    "Use copper-based fungicides and remove infected leaves.",
    "What is Rust disease?",
    "Rust is a fungal disease affecting wheat and other plants, causing orange or brown pustules on leaves.",
    "How to control Rust disease?",
    "Apply fungicides like Mancozeb and rotate crops to break the disease cycle.",
    "How to treat Powdery Mildew?",
    "Use sulfur-based fungicides and prune infected leaves.",
    "How to improve soil health?",
    "Add organic compost, avoid overuse of fertilizers, and rotate crops regularly."
]
"""
csv_file = "mira_plant_disease_training.csv"  # Make sure this file is in the same folder
df = pd.read_csv(csv_file)

# Prepare training data
training_data = []
for index, row in df.iterrows():
    training_data.append(row["Question"])
    training_data.append(row["Answer"])

trainer.train(training_data)

data=open('greetings.yml','r',encoding='utf-8').readlines()
trainer.train(data)
def botReply():
    question=questionField.get()
    question=question.capitalize()
    answer=bot.get_response(question)
    textArea.insert(END,"You:"+question+"\n\n")
    textArea.insert(END, "Mira:" + str(answer)+"\n\n")
    # pyttsx3.speak(answer)
    engine.say(str(answer))
    engine.runAndWait()
    speak(str(answer))

    questionField.delete(0,END)

def audioToText():
    while True:
        sr=speech_recognition.Recognizer()
        try:
            with speech_recognition.Microphone() as m:
                sr.adjust_for_ambient_noise(m, duration=0.2)
                audio = sr.listen(m)
                query = sr.recognize_google(audio)
                query = query.capitalize()

                questionField.delete(0, END)
                questionField.insert(0, query)
                botReply()
                time.sleep(2)
        except Exception as e:
            print(e,"Sorry an Error occured")
# to call  the function audioText we will use concept of threading




root = Tk()
root.config(bg="sea Green")
root.title("\tMira-Chatbot")
root.geometry("500x570")
# Open the image using PIL
image = Image.open("pic.jpeg")
image = image.resize((128, 128),Image.LANCZOS)
photo = ImageTk.PhotoImage(image)

label = Label(root, image=photo,bg="sea green")
label.pack()

centerFrame=Frame(root)
centerFrame.pack()

scrollbar=Scrollbar(centerFrame)
scrollbar.pack(side=RIGHT)

textArea=Text(centerFrame,font=('Arial',20),height=12,yscrollcommand=scrollbar.set,wrap="word")
textArea.pack()
scrollbar.config(command=textArea.yview)

questionField=Entry(root,font=('arial',20,'bold'))
questionField.pack(pady=20,padx=10,fill=X)


# askPic=Image.open('ask.jpeg')
# askPic=askPic.resize((128,128),Image.LANCZOS)
# photo2= ImageTk.PhotoImage(askPic)

# label2 = Label(root, image=photo2,bg="sea green")
# label2.pack()

askButton=Button(root,text="Ask Mira",command=botReply)
askButton.pack()
def click():
    askButton.invoke()
root.bind('<Return>',click())
thread=threading.Thread(target=audioToText)
thread.setDaemon(True)
thread.start()
root.mainloop()
