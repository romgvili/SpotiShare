import socket
import threading
import queue
import time
import spotipy

global songslist
songslist = []
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
        self.client = client
        self.adress = addres
        self.size = 1024

    def run(self):
        global songslist, t, cur,x,until
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
                    if data == "song is done":
                        print("X")
                        if until !=-5:
                            if time.perf_counter()-until<5:
                                self.client.send((t+"!").encode())
                            else:
                                t = songslist[0]
                                until = time.perf_counter()
                                until = time.perf_counter()
                                self.client.send(t.encode())
                                cur = current_milli_time()
                                songslist.remove(t)
                        else:
                                t = daJoker
                                self.client.send(daJoker.encode())
                                cur = current_milli_time()
                                until = time.perf_counter()
                    else:
                        print(data)
                        songslist.append(data)
                        self.client.send("added".encode())




            except:
                return False


if __name__ == "__main__":
    global x
    global t
    t = daJoker
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
