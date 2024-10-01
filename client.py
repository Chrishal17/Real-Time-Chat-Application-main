"""# import required modules
import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox

HOST = '127.0.0.1'
PORT = 1234

DARK_GREY = '#121212'
MEDIUM_GREY = '#1F1B24'
OCEAN_BLUE = '#464EB8'
WHITE = "white"
FONT = ("Helvetica", 17)
BUTTON_FONT = ("Helvetica", 15)
SMALL_FONT = ("Helvetica", 13)

# Creating a socket object
# AF_INET: we are going to use IPv4 addresses
# SOCK_STREAM: we are using TCP packets for communication
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def add_message(message):
    message_box.config(state=tk.NORMAL)
    message_box.insert(tk.END, message + '\n')
    message_box.config(state=tk.DISABLED)

def connect():

    # try except block
    try:

        # Connect to the server
        client.connect((HOST, PORT))
        print("Successfully connected to server")
        add_message("[SERVER] Successfully connected to the server")
    except:
        messagebox.showerror("Unable to connect to server", f"Unable to connect to server {HOST} {PORT}")

    username = username_textbox.get()
    if username != '':
        client.sendall(username.encode())
    else:
        messagebox.showerror("Invalid username", "Username cannot be empty")

    threading.Thread(target=listen_for_messages_from_server, args=(client, )).start()

    username_textbox.config(state=tk.DISABLED)
    username_button.config(state=tk.DISABLED)

def send_message():
    message = message_textbox.get()
    if message != '':
        client.sendall(message.encode())
        message_textbox.delete(0, len(message))
    else:
        messagebox.showerror("Empty message", "Message cannot be empty")

root = tk.Tk()
root.geometry("600x600")
root.title("Messenger Client")
root.resizable(False, False)

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=4)
root.grid_rowconfigure(2, weight=1)

top_frame = tk.Frame(root, width=600, height=100, bg=DARK_GREY)
top_frame.grid(row=0, column=0, sticky=tk.NSEW)

middle_frame = tk.Frame(root, width=600, height=400, bg=MEDIUM_GREY)
middle_frame.grid(row=1, column=0, sticky=tk.NSEW)

bottom_frame = tk.Frame(root, width=600, height=100, bg=DARK_GREY)
bottom_frame.grid(row=2, column=0, sticky=tk.NSEW)

username_label = tk.Label(top_frame, text="Enter username:", font=FONT, bg=DARK_GREY, fg=WHITE)
username_label.pack(side=tk.LEFT, padx=10)

username_textbox = tk.Entry(top_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=23)
username_textbox.pack(side=tk.LEFT)

username_button = tk.Button(top_frame, text="Join", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=connect)
username_button.pack(side=tk.LEFT, padx=15)

message_textbox = tk.Entry(bottom_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=38)
message_textbox.pack(side=tk.LEFT, padx=10)

message_button = tk.Button(bottom_frame, text="Send", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=send_message)
message_button.pack(side=tk.LEFT, padx=10)

message_box = scrolledtext.ScrolledText(middle_frame, font=SMALL_FONT, bg=MEDIUM_GREY, fg=WHITE, width=67, height=26.5)
message_box.config(state=tk.DISABLED)
message_box.pack(side=tk.TOP)


def listen_for_messages_from_server(client):

    while 1:

        message = client.recv(2048).decode('utf-8')
        if message != '':
            username = message.split("~")[0]
            content = message.split('~')[1]

            add_message(f"[{username}] {content}")
            
        else:
            messagebox.showerror("Error", "Message recevied from client is empty")

# main function
def main():

    root.mainloop()
    
if __name__ == '__main__':
    main()


    #"""



import tkinter as tk
from tkinter import messagebox
import time

class TypingSpeedTest:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Test")
        
        self.sample_text = ("The quick brown fox jumps over the lazy dog. "
                            "Typing speed is measured in words per minute (WPM). "
                            "Accuracy is measured by comparing the input with the sample text.")
        
        self.start_time = 0
        self.end_time = 0

        self.setup_ui()
    
    def setup_ui(self):
        self.label = tk.Label(self.root, text="Type the following text:")
        self.label.pack(pady=10)
        
        self.text_area = tk.Text(self.root, height=5, wrap='word', padx=10, pady=10)
        self.text_area.insert(tk.END, self.sample_text)
        self.text_area.configure(state='disabled')
        self.text_area.pack(pady=10)
        
        self.entry = tk.Entry(self.root, width=100)
        self.entry.pack(pady=10)
        self.entry.bind("<KeyPress>", self.start_timer)
        
        self.submit_button = tk.Button(self.root, text="Submit", command=self.calculate_results)
        self.submit_button.pack(pady=10)
    
    def start_timer(self, event):
        if self.start_time == 0:
            self.start_time = time.time()
    
    def calculate_results(self):
        self.end_time = time.time()
        input_text = self.entry.get()
        
        time_taken = self.end_time - self.start_time
        time_taken_minutes = time_taken / 60
        
        word_count = len(input_text.split())
        wpm = word_count / time_taken_minutes
        
        correct_chars = sum(1 for i, c in enumerate(input_text) if i < len(self.sample_text) and c == self.sample_text[i])
        accuracy = correct_chars / len(self.sample_text) * 100
        
        self.show_results(wpm, accuracy)
    
    def show_results(self, wpm, accuracy):
        messagebox.showinfo("Results", f"Words per minute (WPM): {wpm:.2f}\nAccuracy: {accuracy:.2f}%")
        self.reset_test()
    
    def reset_test(self):
        self.start_time = 0
        self.end_time = 0
        self.entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = TypingSpeedTest(root)
    root.mainloop()
