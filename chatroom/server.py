from socket import *
import time, select, random, datetime
from math import *

#the function gets an open port
def get_open_port():
    s = socket(AF_INET, SOCK_STREAM)
    s.bind(("",0))
    s.listen(1)
    port = s.getsockname()[1]
    s.close()
    return port
        
#the function adds the server to the port server
def update_port_server(ip, port):
    port_server_addr = (gethostbyname(gethostname()), 55555)
    port_socket = socket(AF_INET, SOCK_STREAM)
    port_socket.connect(port_server_addr)
    msg = f'add:{NAME}:{ip}:{port}'
    port_socket.send(msg.encode())
    print(f'PORT SERVER SAYS: {port_socket.recv(BUFSIZ).decode()}')
    port_socket.close()

#the function deletes the server from the port server
def delete_port_server():
    port_server_addr = (gethostbyname(gethostname()), 55555)
    port_socket = socket(AF_INET, SOCK_STREAM)
    port_socket.connect(port_server_addr)
    msg = f'del:{NAME}'
    port_socket.send(msg.encode())
    print(f'PORT SERVER SAYS: {port_socket.recv(BUFSIZ).decode()}')
    port_socket.close()

#the function returns date and time
def date():
    time = datetime.datetime.now()
    print_time = time.strftime("%d/%m/%Y %H:%M")
    return print_time

#the function returns a compliment from compliments list
def compliment():
    return random.choice(compliments)

#the function calculates wakeup time and sends a message to the client if needed
def wakeup():
    for s in wake_up:
        if int(time.time()) - int(wake_up[s][0]) > int(wake_up[s][1]):
            try:
                wake_up[s][0] = time.time()
                wake_up[s][1] += 10
                s.send(random.choice(wakeup_msg).encode())
            except:
                continue
                          
#the function returns a quote from quotes list
def send_quote():  
    return random.choice(quotes)

def joke():
    return random.choice(jokes)

BUFSIZ = 1024
NAME = 'HILA'

#tries to connect to open port of the port server and creates a socket
try:
    delete_port_server() 
    HOST = gethostbyname(gethostname())
    PORT = get_open_port()
    

    update_port_server(HOST, PORT)
    ADDR=(HOST,PORT)
    server_sock = socket(AF_INET,SOCK_STREAM)
    server_sock.bind(ADDR)
    server_sock.listen(2)
    sockets = [server_sock]
except:
    print("you need to connect to port server first")
    quit()


#assigning variables
write_sock = []
password = random.randint(1000, 10000)
print(ADDR)
print(f'Admin password: {password}')

send_admin = "Hiloola1234"
wake_up = {}
shut_down = False
users = {}
first_login ={}
wakeup_msg = ["WHERE ARE YOU? WAKE UP!", "Wake up!!", "Are you asleep?",
              "Where are you? :(", "Is everything okay?"]

compliments = ["you are a star!", "you are on fire!", "wowwww!!!",
                   "you look amazing!", "the truck with the prizes is on its way!",
                   "aside from food, you're my favorite."]

quotes = ['“The purpose of our lives is to be happy.” — Dalai Lama',
          '“Life is like riding a bicycle. To keep your balance, you must keep moving.” — Albert Einstein',
          '“The two most important days in your life are the day you are born and the day you find out why.” – Mark Twain',
          '"The way to get started is to quit talking and begin doing." -Walt Disney',
          '"It is during our darkest moments that we must focus to see the light." -Aristotle',
          '"Everything you can imagine is real." – Pablo Picasso',
          '"What we think, we become." – Buddha',
          '"Let the beauty of what you love be what you do." – Rumi',
          '“Stop acting so small. You are the universe in ecstatic motion.”― Rumi',
          '“You were born with wings, why prefer to crawl through life?”― Rumi',
          '"A fish that is dry, will knows the price of water" - Saadi',
          '"Have patience. All things are difficult before they become easy." - Saadi']

jokes = ['What’s the best thing about Switzerland? I don’t know, but the flag is a big plus.',
         'Why don’t scientists trust atoms? Because they make up everything.',
         'What do you call a fake noodle? An impasta',
         'What do you call a magic dog? A labracadabrador',
         'What did the shark say when he ate the clownfish? This tastes a little funny.',
         "What do you call a programmer from Finland? -Nerdic",
         "Why do Java programmers have to wear glasses? Because they don't C#",
         'What do you call a Russian that enjoy programming? Computin',
         'Why Programmers like dark mode? Because light attracts bugs']

while 1:
    #handles connection
    readable, writeable, _ = select.select(sockets, write_sock, [])
    for s in readable:
        if s == server_sock:
            clientsock, addr = server_sock.accept()
            print ('...connected from:', addr)
            sockets.append(clientsock)
            write_sock.append(clientsock)
            wake_up.update({clientsock: [time.time(), 10]})
            first_login.update({clientsock: True})
            print('waiting for connection...')
        else:
            try:
                data = s.recv(BUFSIZ)
                wake_up[s][0] = time.time()
            except:
                s.close()
                sockets.remove(s)
                write_sock.remove(s)
                print(f'client left')
                continue
            
            #handles different functions
            if 'QUIT:' in data.decode():
                data_password = data.decode()[data.decode().index("QUIT:")+6:]
                if data_password==password:
                    s.send("QUIT".encode())
                    for socket in writeable:
                        socket.close()
                    server_sock.close()
                    quit() 
                else:
                    messages[clientsock].append("wrong password".encode())
            elif first_login[s] == True:
                users.update({s: data.decode()})
                first_login.update({s: False})
            elif 'TIME' in data.decode():
                s.send(f'time: {date()}'.encode())
            elif 'ADM:' in data.decode():
                admin = data.decode()[data.decode().index("ADM:")+4:].replace(" ","")
                print(admin)
                if admin == send_admin:
                    s.send(f'admin password is: {password}'.encode())
            elif 'CONN' in data.decode():
                s.send(f'there are {len(writeable)} users connected'.encode())
            elif "BR" in data.decode():
                for sock in writeable:
                    msg = data.decode().replace('BR', '')
                    sock.send(msg.encode())
            elif "From" in data.decode():
                data_decode = data.decode()
                name = data_decode[data_decode.index("SEND TO")+8:data_decode.index(": ")]
                for key, item in users.items():
                    if name == item:
                        msg = data.decode().replace(f'SEND TO {item}:', '')
                        key.send(msg.encode())
            elif "kicked" in data.decode():
                data_decode = data.decode()
                name = data_decode[data_decode.index("kicked")+7:]
                print(name)
                for key, item in users.items():
                    if name == item:
                        key.send("sorry, you have been kicked :(".encode())
                        key.close()
                        sockets.remove(key)
                        write_sock.remove(key)
            elif "CALC" in data.decode():
                equation = data.decode()[data.decode().index("CALC:")+5:]
                print(equation)
                try:
                    equation_result = eval(equation)
                    s.send(("solution is: " + str(equation_result)).encode())
                except ValueError:
                    s.send("can't calculate the equation".encode())
                    
            elif 'COM' in data.decode():
                s.send(compliment().encode())
            elif "QOTD" in data.decode():
                s.send(send_quote().encode())
            elif "JOKE" in data.decode():
                s.send(joke().encode()
            else:
                s.send(data)
    wakeup()
    
delete_port_server()    
server_sock.close()

    

