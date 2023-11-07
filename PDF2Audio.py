import PyPDF2 #extracting text
from tkinter import * #GUI
from tkinter import messagebox as mbox #GUI error message
from pydub import AudioSegment #segmenting audio files
import os #deleting files
from googletrans import Translator
from gtts import gTTS

def pdf_to_aud_trans():
    audioclips = [] #list containing address of each audiofile
    translator = Translator() #handler variable for GTTS
    direc = str(path_field.get()) #variable for PDF path
    path = open(direc, 'rb') #file handler variable
    lng = str(clicked.get()) #variable containing selected language
    # creating a PdfFileReader object
    pdfReader = PyPDF2.PdfReader(path)
    # this will read the page of 1st page.
    page = int(page_field.get())
    page_end = int(page_field2.get())
    audio = str(direc_field.get())
    for i in range(page,page_end+1):
        audiox = audio +str(i)
        from_page = pdfReader.pages[i-1]                 
        # extracting the text from the PDF
        text = from_page.extract_text() #contains all text from a selected page
        translated_text = translator.translate(text, dest = lng) #contains translated text of selected language of each page
        ttmp3 = gTTS(translated_text.text, lang = lng) #file handler that contains the converted audiofile
        ttmp3.save(audiox + ".mp3") #saving audiofile of translated text of each page
        audioclips.append(str(os.getcwd()) + '\\' + audiox  + ".mp3")
    final_audio = AudioSegment.from_file(file = audioclips[0], format = "mp3")
    for i in range(1,len(audioclips)):
        soundx = AudioSegment.from_file(file = audioclips[i], format = "mp3")
        final_audio = final_audio + soundx
    final_audio.export(audio + ".mp3", format = "mp3")
    for i in range(0,len(audioclips)):
        os.remove(audioclips[i])

def clear_all():
    path_field.delete(0, END)
    page_field.delete(0, END)
    direc_field.delete(0, END)
    page_field2.delete(0,END)

if __name__ == "__main__" :

    root = Tk()
    root.iconbitmap(r'C:\Users\shree\Downloads\audiobook.ico')
    root.configure(background = '#abcacf')
    root.geometry("400x310")
    root.title("PDF TO AUDIO CONVERTER")
    #Labels
    label1 = Label(root, text = "Enter PDF directory : ",fg = 'black', bg = '#499959')
    label2 = Label(root, text = "Enter page to convert : ",fg = 'black', bg = '#499959')
    label3 = Label(root, text = "Enter till which page to convert : ",fg = 'black', bg = '#499959')
    label4 = Label(root, text = "Enter name to save : ",fg = 'black', bg = '#499959')
    label5 = Label(root, text = "Choose language : ",fg = 'black', bg = '#499959')
    options = ["en","hi","ta","te","ch","ja"]
    clicked = StringVar()
    clicked.set("en")

    label1.grid(row = 1, column = 0, padx = 10, pady = 10)
    label2.grid(row = 2, column = 0, padx = 10, pady = 10)
    label3.grid(row = 3, column = 0, padx = 10, pady = 10)
    label4.grid(row = 4, column = 0, padx = 10, pady = 10)
    label5.grid(row = 5, column = 0, padx = 10, pady = 10)
    drop = OptionMenu(root, clicked, *options)
    #Input fileds
    path_field = Entry(root)
    page_field = Entry(root)
    page_field2 = Entry(root)
    direc_field = Entry(root)

    path_field.grid(row = 1, column = 1, padx = 10, pady = 10)
    page_field.grid(row = 2, column = 1, padx = 10, pady = 10)
    page_field2.grid(row = 3, column = 1, padx = 10, pady = 10)
    direc_field.grid(row = 4, column = 1, padx = 10, pady = 10)
    drop.grid(row = 5, column = 1, padx = 10, pady = 10)
    drop.config(width = 10)
    #Buttons
    button1 = Button(root, text = "Create Audio", bg = "#2c3bb0", fg = "white", command = pdf_to_aud_trans)
    button2 = Button(root, text = "Clear", bg = "#2c3bb0", fg = "white", command = clear_all)

    button1.grid(row = 8, column = 1, pady = 10)
    button2.grid(row = 10, column = 1, pady = 10)

    root.mainloop()
