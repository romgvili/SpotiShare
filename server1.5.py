import socket
import threading
import os
import time
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sys

global songslist, first,count,next
count=0
songslist = []
next = ""
first = False
text = ""
user = ""
clients = set()
clients_lock = threading.Lock()
def connecet():
    global sp
    client_credentials_manager = SpotifyClientCredentials('221e9a5fac5c4f40bb2de9c33ce7a863',
                                                          '8c5e85b7165840bbb605b43924952889')
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
def connect():
    try:
        connecet()
    except:
        connect()
until = -5
def current_milli_time():
    return (round(time.time() * 1000))


daJoker = "spotify:track:4uLU6hMCjMI75M1A2tKUQC"


class ThreadedServer(threading.Thread):
    def __init__(self, host, port):
        super(ThreadedServer, self).__init__()
        self.plist = []
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def run(self):
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            p = listenToClient(client, address)
            p.start()
            self.plist.append(p)
            with clients_lock:
                clients.add(client)


class listenToClient(threading.Thread):
    def __init__(self, client, addres):
        super(listenToClient, self).__init__()
        self.lock = threading.Lock()
        self.client = client
        self.adress = addres
        self.size = 1024

    def run(self):
        global songslist, t, cur,x,until, tlen, next, count
        print('runnung ', self.adress)
        self.client.send(("connected successfully").encode())
        self.client.sendall(x.encode())
        if x == "T":
            time.sleep(0.5)
            self.client.sendall(t.encode())
            time.sleep(0.5)
            self.client.sendall(str(current_milli_time()-cur).encode())
        x = "T"
        while True:
            if next != "":
                with clients_lock:
                    for c in clients:
                        if count ==0:
                            print("A")
                            c.sendall(("next " + t).encode())
                            cur = current_milli_time()
                            until = time.perf_counter()
                            count+=1
                        else:
                            print("a")
                            c.sendall(("next "+t+str(current_milli_time()-cur)).encode())
                            count+=1

                count=0
                next=""
            try:
                data = self.client.recv(self.size)
                data = data.decode('UTF8')
                if data:
                    self.lock.acquire()
                    if data == "song is done":
                        print("X")
                        if until !=-5:
                            if time.perf_counter()-until<tlen-10:
                                print("A")
                                self.client.send((t+"! "+str(cur)).encode())
                            else:
                                if songslist:
                                    t = songslist[0]
                                    until = time.perf_counter()
                                    self.client.send(t.encode())
                                    cur = current_milli_time()
                                    songslist.remove(t)
                                    tlen = sp.track(t)['duration_ms'] / 1000
                                else:
                                    t = daJoker
                                    self.client.send(daJoker.encode())
                                    cur = current_milli_time()
                                    until = time.perf_counter()
                                    tlen = sp.track(t)['duration_ms'] / 1000


                    elif data[0:5] == "start":
                        t = "spotify:track:"+data[5:]
                        self.client.send(t.encode())
                        cur = current_milli_time()
                        until = time.perf_counter()
                        tlen = sp.track(t)['duration_ms'] / 1000
                    elif "spotify:" in data:
                        print(data)
                        songslist.append(data)
                        self.client.send("added".encode())
                    elif "play next song" in data:
                        print("1")
                        if songslist:
                            print("2")
                            t = songslist[0]
                            next= t
                            songslist.remove(t)
                            tlen = sp.track(t)['duration_ms'] / 1000
                        else:
                            print("3")
                            t = daJoker
                            next = (t)
                            tlen = sp.track(t)['duration_ms'] / 1000
                    elif "sms " in data:
                        with clients_lock:
                            for c in clients:
                                c.sendall((data).encode())


                    self.lock.release()





            except:
                return False


if __name__ == "__main__":
    connect()
    global x
    global t
    global tlen
    t = daJoker
    tlen = sp.track(t)['duration_ms']/1000
    print(tlen)
    x = "F"
    while True:
        port_num = 8000
        try:
            port_num = int(port_num)
            break
        except ValueError:
            pass

    Ts = ThreadedServer('0.0.0.0', port_num)
    Ts.start()
    Ts.join()
