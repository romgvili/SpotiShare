import socket
import threading
import os
import time
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sys

global songslist
songslist = []
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


class listenToClient(threading.Thread):
    def __init__(self, client, addres):
        super(listenToClient, self).__init__()
        self.lock = threading.Lock()
        self.client = client
        self.adress = addres
        self.size = 1024

    def run(self):
        global songslist, t, cur,x,until, tlen
        print('runnung ', self.adress)
        self.client.send(("connected successfully").encode())
        self.client.sendall(x.encode())
        if x == "T":
            time.sleep(0.5)
            self.client.sendall(t.encode())
            time.sleep(0.5)
            self.client.sendall(str(cur).encode())
        x = "T"
        while True:
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
                                    print("B")
                                    t = songslist[0]
                                    until = time.perf_counter()
                                    self.client.send(t.encode())
                                    cur = current_milli_time()
                                    songslist.remove(t)
                                    tlen = sp.track(t)['duration_ms'] / 1000
                                else:
                                    print("C")
                                    t = daJoker
                                    self.client.send(daJoker.encode())
                                    cur = current_milli_time()
                                    until = time.perf_counter()
                                    tlen = sp.track(t)['duration_ms'] / 1000


                        else:
                            print("D")
                            t = daJoker
                            self.client.send(daJoker.encode())
                            cur = current_milli_time()
                            until = time.perf_counter()
                            tlen = sp.track(t)['duration_ms'] / 1000
                    else:
                        print(data)
                        songslist.append(data)
                        self.client.send("added".encode())
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
