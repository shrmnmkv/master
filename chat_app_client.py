import socket
import threading
import tkinter as tk
from tkinter import ttk
from googletrans import Translator

# Client configuration
HOST = socket.gethostbyname(socket.gethostname())
PORT = 9999

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            message = "Received: " + message
            update_chat_history(message)
        except:
            break

def send_message():
    message = message_entry.get()
    if message:
        target_language = language_var.get()  # Get the selected language
        translated_message = translator.translate(message, dest=target_language).text
        update_chat_history("Sent: " + message)
        update_chat_history(f"Translated ({target_language}): " + translated_message)
        client.send(translated_message.encode('utf-8'))
        message_entry.delete(0, tk.END)

def apply_translation_language():
    target_language = language_var.get()
    translator = Translator()
    translator.target_lang = target_language
    update_chat_history("Translation language updated to " + target_language)

def update_chat_history(message):
    chat_history.config(state=tk.NORMAL)
    chat_history.insert(tk.END, message + '\n')
    chat_history.config(state=tk.DISABLED)
    chat_history.see(tk.END)  # Scrolls to the bottom of the chat history

if __name__ == '__main__':
    global client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.start()

    translator = Translator()
    
    root = tk.Tk()
    root.title("Chat Application")

    language_label = tk.Label(root, text="Select Translation Language:")
    language_label.pack()

    language_var = tk.StringVar()
    language_combobox = ttk.Combobox(root, textvariable=language_var, values=["en", "fr", "es", "te", "ta"])  # Add more languages as needed
    language_combobox.set("en")  # Default language to English
    language_combobox.pack()

    chat_frame = tk.Frame(root)
    chat_frame.pack()

    chat_history = tk.Text(chat_frame, state=tk.DISABLED, wrap=tk.WORD)
    chat_history.pack(side=tk.LEFT)

    chat_scrollbar = tk.Scrollbar(chat_frame, command=chat_history.yview)
    chat_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    chat_history.config(yscrollcommand=chat_scrollbar.set)

    apply_language_button = tk.Button(root, text="Apply Language", command=apply_translation_language)
    apply_language_button.pack()

    message_entry = tk.Entry(root)
    message_entry.pack()

    send_button = tk.Button(root, text="Send", command=send_message)
    send_button.pack()

    root.mainloop()
