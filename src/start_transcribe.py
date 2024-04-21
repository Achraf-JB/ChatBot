import time
from googletrans import Translator
import pyaudio
from vosk import Model,KaldiRecognizer
from src.tools import Tools
from src.arabic_chat import Chat
from src.send_image.pipeline.final_stage import SendPipeline
import pywhatkit

tool = Tools()
trans = Translator()
arabic = Chat()



english_model = r"C:\Users\HP\OneDrive\Bureau\chatbot\models\vosk-model-small-en-us-0.15\vosk-model-small-en-us-0.15"
french_model = r"C:\Users\HP\OneDrive\Bureau\chatbot\models\vosk-model-small-fr-0.22\vosk-model-small-fr-0.22"




class vosk_chat():

    def __init__(self,file_path):
        self.file_path = file_path
        self.text = None
        self.language = "en"

        self.english_model_path = english_model
        self.french_model_path = french_model
        self.count_silence = 0

        self.model_english = Model(self.english_model_path)
        self.recognizer_english = KaldiRecognizer(self.model_english, 16000)
        print("english model set successfully")
        self.model_french = Model(self.french_model_path)
        self.recognizer_french = KaldiRecognizer(self.model_french, 16000)
        print("french model set successfully")

        # Initialize PyAudio instance and stream
        self.mic = pyaudio.PyAudio()
        self.stream = self.mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
        self.stream.start_stream()

    def listen(self):

        while (1):
            data = self.stream.read(10240)
            if self.recognizer_english.AcceptWaveform(data):
                tex = self.recognizer_english.Result()
                self.text = tex[13:len(tex)-2]

                self.text = tool.translate(self.text)

                print(self.text)

                if ( len(self.text)>3):
                    self.count_silence = 0
                    break
                else:

                    if (self.count_silence > 10):
                        self.main_()
                    self.count_silence += 1

            time.sleep(0.2)

    def listen_french(self):

        while (1):
            data = self.stream.read(10240)
            if self.recognizer_french.AcceptWaveform(data):
                tex = self.recognizer_french.Result()
                self.text = tex[13:len(tex)-2]

                self.text = tool.translate(self.text)

                print(self.text)

                if ( len(self.text)>3):
                    self.count_silence = 0
                    break
                else:

                    if (self.count_silence > 10):
                        self.main_()
                    self.count_silence += 1

            time.sleep(0.2)





    def treatment(self):
        if "hello" in self.text:
            response = "Hello, can i help you"

            self.speak_(response)

        if "language" in self.text:
            self.provided_lang()


        if ("english" in self.text) :
            self.language = "en"
            tool.speak("let's speak english !!")

        if ("fran" in self.text  or "fren" in self.text) :
            self.language = "fr"
            tool.speak_french("on parle francais alors !")

        if ("arabic" in self.text) :
            self.language = "ar"
            tool.speak_french("on parle arabe alors !")

        if("picture" in self.text):
            response = "ladies and gentelmens let's take a picture for memory now !! "
            self.speak_(response)
            send = SendPipeline(self.file_path)
            send.main()

        if("play" in self.text):
            response = "playing musique"
            self.speak_(response)
            pywhatkit.playonyt(self.text) 

        # if ('who the heck is' in self.text): 
        #         person = self.text.replace('who the heck is', '')
        #         info = wikipedia.summary(person, 1)
        #         self.speak_(info)
        # if 'date' in self.text:
        #         self.speak_('sorry, I have a headache')
        # if 'are you single' in self.text:
        #         self.speak_('I am in a relationship with wifi')
        # if 'joke' in self.text:
        #         self.speak_(pyjokes.get_joke())
        else:
                
                self.speak_("Sorry, I didn't understand that command.")     






    def start_listening(self):
        self.listen()
        if("alexa" in self.text):
            return True


    def main_(self):

        while (not self.start_listening()):
            time.sleep(0.1)

        help_sentence = "how can i help you sir"
        if(self.language == "en"):
            tool.speak(help_sentence)
        else:
            tool.speak_french(tool.translate_french(help_sentence))


        while 1:
            if not tool.isSpeaking:
                if(self.language == 'en'):
                    self.listen()
                elif(self.language == 'fr'):
                    self.listen_french()
                else:
                    self.text = arabic.reconise(5)
                    print(self.text)

                self.run_from_none()
                self.treatment()
            time.sleep(0.1)


    def run_from_none(self):
        if self.text is None:
            print(self.text)
            self.text = "c"





    def change_language(self):


        self.listen()

        if("arabic" in self.text):
            self.language = 'ar'
            tool.speak_french("on parle arabe alors !")
            return

        elif("fren" in self.text or "fran" in self.text):
            self.language = 'fr'
            tool.speak_french("on parle français alors !")
            return

        elif("english" in self.text):
            self.language = 'en'
            tool.speak("let's speak english !!")
            return

        else:
            self.change_language()



    def provided_lang(self):
        if (self.language == 'en'):
            tool.speak("choose between frensh or arabic !")
        elif (self.language == 'fr'):
            tool.speak_french("choisissez entre l'arabe et l'anglais !")
        elif (self.language == 'ar'):
            tool.speak_french("choisissez entre le francais et l'anglais !")


    def speak_(self,response):


        if (self.language == "en"):
            tool.speak(response)
        else:
            response = tool.translate_french(response)
            print(response)
            tool.speak_french(response)
