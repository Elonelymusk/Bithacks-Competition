import tkinter as tk
import time 

root = tk.Tk()
TextBox = tk.Text(root, height = 20, width = 70)
TextBox.pack(side=tk.LEFT, fill=tk.Y)
ScrollBar = tk.Scrollbar(root)
ScrollBar.pack(side=tk.RIGHT, fill=tk.Y)
InputBox = tk.Entry(root)
InputBox.pack(side=tk.BOTTOM, fill=tk.X)


def chatbot_response(response):
    InputBox.delete(first = 0, last = 10000)
    TextBox.insert(tk.END, "Bot:" + response + "\n")


def user_input():
    #function called when the button is pressed
    #Reads input in entry widget and prints onto text widget
    user_input = InputBox.get()
    InputBox.delete(first = 0, last = 10000)
    TextBox.insert(tk.END, "User:" + user_input + "\n")

SendButton = tk.Button(root, text="SEND", command = user_input)
SendButton.pack(side=tk.BOTTOM)

while True:
    with open("response_file.txt", "r") as response_file:
        message = response_file.read()
        chatbot_response(message)
        response_file.close()
    root.update_idletasks()
    root.update()
