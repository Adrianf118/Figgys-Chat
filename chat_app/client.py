from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter

# funtion to receive
def receive():
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(tkinter.END, msg)
        except OSError:  
            break

# function to send
def send(event=None): 
    msg = my_msg.get()
    my_msg.set("")  # Clears input field.
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()
        top.quit()

#fucntion to close application
def on_closing(event=None):
    my_msg.set("{quit}")
    send()

top = tkinter.Tk()
top.title("Figgy's Chat!")

messages_frame = tkinter.Frame(top)

# so message can be sent
my_msg = tkinter.StringVar()  
my_msg.set("")

# to scroll through previous messages
scrollbar = tkinter.Scrollbar(messages_frame) 
# this will contain the messages.
msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)

# user input to connect to chat
HOST = input('Enter host: ') 
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()  