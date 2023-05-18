"""
Author: Hila Rahimipour
Homework excercise 6
the program is the client side of a chat room
"""

#import libraries
from socket import *
import select, threading
from tkinter import *
from tkinter import font
from datetime import datetime

#function tries to connect to the port server and to the server itself
def get_server_info():
    port_server_addr = (gethostbyname(gethostname()), 55555)
    port_socket = socket(AF_INET, SOCK_STREAM)
    port_socket.connect(port_server_addr)
    port_socket.send(f'get:{NAME}'.encode())
    addr = port_socket.recv(BUFSIZ).decode()
    if addr == 'no':
        listbox.insert(END, "server doesn't exist")
        root.after(1000, exit())
        quit()
    else:
        return eval(addr)

#function recieves data from the server
def receive():
    while 1: 
        try:
            data = client_sock.recv(BUFSIZ).decode('utf8')
            if data != '':
                listbox.insert(END, data)
                listbox.see("end")
            else:
                break
            if data == "QUIT":
                listbox.insert(END, "server shut down")
                listbox.see("end")
                root.after(500, exit())
            if data == "sorry, you have been kicked :(":
                listbox.insert(END, "sorry, you have been kicked :(")
                listbox.see("end")
                root.after(500, exit())
        except OSError:
            client_sock.close()
        except:
            pass
    exit()

#the function closes the socket and the program
def exit_client():
    try:
        client_sock.close()
        root.destroy()
    except:
        pass
    
#the fuction handles the messages sent to the server and sends them to the server
def send_msg(event=None):
    global is_first, client
    data = client_msg.get()
    client_msg.set("")
    now = datetime.now()
    time = now.strftime("%H:%M")

    if is_first:
        client = data
        listbox.insert(END, f'{client} Welcome to my chat server! Nice to see you!')
        listbox.see("end")
        is_first = False
        try:
            client_sock.send(data.encode())
        except:
            pass
    elif data=="":
        listbox.insert(END, "you must enter a message")
        listbox.see("end")
    elif data == 'EXIT':
        try:
            client_sock.send("EXIT".encode())
        except:
            pass
        listbox.insert(END, f' Goodbye {client} :( Hope to see you again!')
        listbox.see("end")
        root.after(1000, exit_client())
    elif "BR" in data:
        try:
            client_sock.send(f'BR[{time}] {client}: {data.replace("BR", "")}'.encode())
        except:
            pass
    elif "SEND TO" in data:
        if ":" in data:
            try:
                client_sock.send(f'[{time}] From {client}- {data}'.encode())
            except:
                pass
            listbox.insert(END, f'[{time}] message sent')
            listbox.see("end")
        else:
            listbox.insert(END, 'please enter in correct format- SEND TO {name}: {message}')
            listbox.see("end")
    elif "ADM" in data:
        if ":" in data:
            try:
                client_sock.send(data.encode())
            except:
                pass
            listbox.insert(END, data)
            listbox.see("end")
        else:
            listbox.insert(END, 'please enter in correct format- ADM: {admin pass}')
            listbox.see("end")
    elif "QUIT" in data:
        if ":" in data:
            try:
                client_sock.send(data.encode())
            except:
                pass
            listbox.insert(END, data)
            listbox.see("end")
        else:
            listbox.insert(END, 'please enter in correct format- QUIT: {password}')
            listbox.see("end")
    elif "KICK" in data:
        kick_name = data[data.index("KICK ")+5:]
        try:
            client_sock.send(f'[{time}] {client} kicked {kick_name}'.encode())
            listbox.insert(END, f'[{time}] {client} kicked {kick_name}')
            listbox.see("end")
        except:
            listbox.insert(END, data)
            listbox.see("end")
    elif "CALC" in data:
        if ":" in data:
            try:
                client_sock.send(data.encode())
            except:
                listbox.insert(END, data)
                listbox.see("end")
        else:
            listbox.insert(END, "please enter in correct format- CALC: {equastion}")
            listbox.see("end")
    else:
        try:
            client_sock.send(f'[{time}] {data}'.encode())
        except:
            listbox.insert(END, f'[{time}] {data}')
            listbox.see("end")
            pass
        
#the function states what would happen if the client closes the program's tab
def on_closing():
    listbox.insert(END, f' Goodbye {client} :( Hope to see you again!')
    listbox.see("end")
    root.after(500, root.destroy())

#creating root and assigning proparties
root = Tk()
root.title("Hila's chat room")
root.maxsize(root.winfo_screenwidth(), root.winfo_screenheight())
root.minsize(600, 400)
root["background"] = "#%02x%02x%02x" % (230, 255, 230)

Label(root, text="Chat Room", font=font.Font(family="Calibri bold", size=20),
      bg="#%02x%02x%02x" % (230, 255, 230)).pack(pady=5)

messages = Frame(root)
scrollbar_y = Scrollbar(messages)
scrollbar_x = Scrollbar(messages, orient=HORIZONTAL)


listbox = Listbox(messages, xscrollcommand=scrollbar_x.set,
                   yscrollcommand=scrollbar_y.set, width=90, height=20)

scrollbar_x.pack(side=BOTTOM, fill=X)
scrollbar_y.pack(side=RIGHT, fill=Y)
listbox.pack(fill=BOTH, side=LEFT)

listbox.insert(END, f'Hello there! please enter your name')
listbox.see("end")

scrollbar_x.config(command=listbox.xview)
scrollbar_y.config(command=listbox.yview)


client_msg = StringVar()
client_msg.set("")
text_entry = Frame(root, bg="#%02x%02x%02x" % (230, 255, 230))
entry = Entry(text_entry, textvariable=client_msg, width=60, font=font.Font(family="Calibri", size=12))

#sends message with "ENTER"
entry.bind("<Return>", send_msg)

entry.grid(row=0, column=0, padx=5, pady=5)
button = Button(text_entry, text="Send", command=send_msg)
button.grid(row=0, column=1, padx=5)

messages.pack(pady=10)
text_entry.pack(pady=10)

#states what happens when tab is closed
root.protocol("WM_DELETE_WINDOW", on_closing)


BUFSIZ = 1024
NAME = 'HILA'

#tries to connect to the server
try:
    ADDR = get_server_info()
    print(ADDR)
    client_sock = socket(AF_INET,SOCK_STREAM)
    client_sock.connect(ADDR)

except:
    listbox.insert(END, f'port server not found, OFFLINE MODE!!')
    listbox.see("end")
    pass
is_first = True
client = ""

#states that the recieve function will run all the time
receive_thread = threading.Thread(target=receive)
receive_thread.daemon = True
receive_thread.start()

root.mainloop()



