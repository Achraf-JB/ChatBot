
import speech_recognition as sr
import pyttsx3
import wikipedia
import pyjokes
import datetime
from src.send_image.pipeline.final_stage import SendPipeline
from src.send_image.components.play_music import Alexa



class Model_pipeline:
    def __init__(self,file_path):
        self.file_path = file_path
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 140)
        self.listener = sr.Recognizer()

    def talk(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def take_command(self):
        command = ""
        try:
            with sr.Microphone() as source:
                print('listening...')
                self.listener.adjust_for_ambient_noise(source,duration=0.2)
                voice = self.listener.listen(source)
                command = self.listener.recognize_google(voice)
                command = command.lower()
        except Exception as e:
            pass
        return command
    
    def run(self):
        command = self.take_command()
        if 'alexa' in command:
            result = command.replace('alexa', '')
            print(result)
            if result == "led_on":
                self.talk("led on")
                # Add your logic to turn on the LED here
            elif result == "led_off":
                self.talk("led off")
                # Add your logic to turn off the LED here
            elif result == "take_photo":
                self.talk("take photo")
                send = SendPipeline(self.file_path)
                send.main()
            elif result == "play_music":
                self.talk("play music")
                alexa = Alexa()
                alexa.run_alexa()
            elif result == "show_background":
                self.talk("show background")
                # Add your logic to show background here
            elif result == "hide_background":
                self.talk("hide background")
                # Add your logic to hide background here
            elif 'time' in command:
                time = datetime.datetime.now().strftime('%I:%M %p')
                self.talk('Current time is ' + time)
            elif 'who the heck is' in command:
                person = command.replace('who the heck is', '')
                info = wikipedia.summary(person, 1)
                print(info)
                self.talk(info)
            elif 'date' in command:
                self.talk('sorry, I have a headache')
            elif 'are you single' in command:
                self.talk('I am in a relationship with wifi')
            elif 'joke' in command:
                self.talk(pyjokes.get_joke())
            else:
                # Handle unknown or unsupported commands
                self.talk("Sorry, I didn't understand that command.")