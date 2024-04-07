import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox
import customtkinter as ctk
from PIL import Image,ImageTk

def receive_messages():
    while True:
        try:
            data = client_socket.recv(1024)
            if data:
                message = data.decode()
                chat_window.insert(tk.END, "[Client 2]: " + message + "\n")
        except Exception as e:
            print(f"Error receiving message: {e}")
            break

def send_message():
    message = message_entry.get().strip()
    if message:
        client_socket.send(message.encode())
        chat_window.insert(tk.END, "[Client 1]: " + message + "\n")
        message_entry.delete(0, tk.END)  # Clear the input box
    else:
        messagebox.showwarning("Empty Message", "Please enter a message.")


def on_close():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        client_socket.close()
        root.destroy()

#HOST = '127.0.0.1'
HOST = '192.168.184.106'  # Loopback address
PORT = 5555

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

root = tk.Tk()
root.title("QText(C1)")

pil_image = Image.open("D:\EVS_2ND_SEM\Send_Image_6.png")
resized_pil_image = pil_image.resize((500, 500))  # Change size as needed
ctk_image = ctk.CTkImage(resized_pil_image)

chat_window = scrolledtext.ScrolledText(root, width=50, height=20,bg = "black",fg = "white")
chat_window.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

message_entry = ctk.CTkEntry(root, width=350,height = 30,placeholder_text="Type here")
message_entry.grid(row=1, column=0, padx=5, pady=5)

send_button = ctk.CTkButton(root, command=send_message,fg_color="blue",text="", image=ctk_image,compound="right",height=30, width=70)
send_button.grid(row=1, column=1, padx=5, pady=5)

root.protocol("WM_DELETE_WINDOW", on_close)

receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

root.mainloop()