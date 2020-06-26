import tkinter as tk
import time


root = tk.Tk()
TextBox = tk.Text(root, height = 20, width = 70)
TextBox.pack(side=tk.LEFT, fill=tk.Y)
ScrollBar = tk.Scrollbar(root)
ScrollBar.pack(side=tk.RIGHT, fill=tk.Y)
InputBox = tk.Entry(root)
InputBox.pack(side=tk.BOTTOM, fill=tk.X)

def UserInput():
    #function called when the button is pressed
    #Reads input in entry widget and prints onto text widget
    UserInput = InputBox.get()
    InputBox.delete(first = 0, last = 10000)
    print(UserInput)
    TextBox.insert(tk.END, "User:" + UserInput + "\n")
    TextBox.insert(tk.END, "Chatbot: You are going to die \n")

SendButton = tk.Button(root, text="SEND", command = UserInput)
SendButton.pack(side=tk.BOTTOM)

while True:
    root.update_idletasks()
    root.update()
