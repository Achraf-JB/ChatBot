import tkinter as tk
from tkinter import filedialog


class BackgroundSelector:
    def __init__(self) :
          self.root = tk.Tk()
          self.root.title("Select Background Image")

    def open(self):
        
        self.filename = filedialog.askopenfilename(initialdir=r"C:\Users\HP\OneDrive\Bureau\chatbot\photo\photo_back",
                                                       title='select file',
                                                       filetypes=(("png files","*.png"),("jpg files","*.jpg"),("all the files","*.*")))
        
        return self.filename  
    def destroy_app(self):
         self.root.destroy() 

