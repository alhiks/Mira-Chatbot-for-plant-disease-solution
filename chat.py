import pandas as pd
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import pyttsx3
import speech_recognition
import threading
import pyaudio
from tkinter import *

# Initialize Mira Chatbot
mira = ChatBot("Mira")

# Load training data from CSV
csv_file = "mira_plant_disease_training.csv"  # Make sure this file is in the same folder
df = pd.read_csv(csv_file)

# Prepare training data
training_data = []
for index, row in df.iterrows():
    training_data.append(row["Question"])
    training_data.append(row["Answer"])

# Train Mira
trainer = ListTrainer(mira)
trainer.train(training_data)

# Initialize Text-to-Speech Engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')

# Select a Female Voice
for voice in voices:
    if "female" in voice.name.lower() or "zira" in voice.name.lower() or "samantha" in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break

# Reduce Speed of Speech
engine.setProperty('rate', 120)


def speak(text):
    engine.say(text)
    engine.runAndWait()


# GUI with Tkinter
def botReply():
    question = questionField.get().capitalize()
    answer = mira.get_response(question)

    textArea.insert(END, "You: " + question + "\n\n")
    textArea.insert(END, "Mira: " + str(answer) + "\n\n")

    speak(str(answer))
    questionField.delete(0, END)


# Voice Input (Speech-to-Text)
def audioToText():
    sr = speech_recognition.Recognizer()
    while True:
        try:
            with speech_recognition.Microphone() as m:
                sr.adjust_for_ambient_noise(m, duration=0.2)
                audio = sr.listen(m)
                query = sr.recognize_google(audio)
                query = query.capitalize()

                questionField.delete(0, END)
                questionField.insert(0, query)
                botReply()
        except Exception as e:
            print("Error:", e)


# Create GUI Window
root = Tk()
root.config(bg="sea Green")
root.title("Mira - Chatbot")
root.geometry("500x570")

centerFrame = Frame(root)
centerFrame.pack()

scrollbar = Scrollbar(centerFrame)
scrollbar.pack(side=RIGHT)

textArea = Text(centerFrame, font=('Arial', 20), height=12, yscrollcommand=scrollbar.set, wrap="word")
textArea.pack()
scrollbar.config(command=textArea.yview)

questionField = Entry(root, font=('arial', 20, 'bold'))
questionField.pack(pady=20, padx=10, fill=X)

askButton = Button(root, text="Ask Mira", font=("Arial", 14), command=botReply)
askButton.pack()


def click():
    askButton.invoke()


root.bind('<Return>', click)

# Start Speech Recognition in Background
thread = threading.Thread(target=audioToText)
thread.setDaemon(True)
thread.start()

root.mainloop()
