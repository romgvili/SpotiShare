import socket

__author__ = 'rom gvili'

import webbrowser
import spotipy
from os import path
import spotipy.util as util
import sys
import keyboard
import time


def current_milli_time():
    return int(round(time.time() * 1000))


def isPlaying():
    try:
        if spoyifyObj.currently_playing()["is_playing"]:
            return True
        return False
    except:
        return False


trackLists = []
address = '127.0.0.1'
port = 8000
bsize = 1024
scope = 'playlist-modify-public streaming user-modify-playback-state user-read-playback-state user-read-currently-playing'
name = input("enter username ")

try:
        if path.exists(f".cache-{name}"):
            file = open(f".cache-{name}")
            text = file.read()
            text= text[270:401]
            token = spotipy.SpotifyOAuth.refresh_access_token(text)
        else:
            token = util.prompt_for_user_token(name, scope,
                                               client_id='221e9a5fac5c4f40bb2de9c33ce7a863',
                                               client_secret='8c5e85b7165840bbb605b43924952889',
                                               redirect_uri='http://google.com/')

except:
        token = util.prompt_for_user_token(name, scope,
                                           client_id='221e9a5fac5c4f40bb2de9c33ce7a863',
                                           client_secret='8c5e85b7165840bbb605b43924952889',
                                           redirect_uri='http://google.com/')

spoyifyObj = spotipy.Spotify(auth=token)
user = spoyifyObj.current_user()


def ChooseDevice():
    global device
    devices = spoyifyObj.devices()
    devices = devices['devices']
    try:
        devices[0]
    except:
        return False
    print("your devices:\n")
    for device in devices:
        print(device['name'])
    name = input("enter device name ")
    for devic in devices:
        if devic['name'] == name:
            device = devic
            return True
    return False
if ChooseDevice()==False:
    print("please open spotify on the desired device and connect")
    time.sleep(5)
    while ChooseDevice()==False:
        time.sleep(5)
displayName = user['display_name']
Followers = user['followers']['total']
print("welcome to spotipy " + displayName)
print("you have " + str(Followers) + " followers")

clientSocket = socket.socket()
clientSocket.connect((address, port))
clientSocket.settimeout(2)
print(clientSocket.recv(22).decode('UTF8'))
x = clientSocket.recv(34).decode('UTF8')
pos =""
def play():
    print(pos+"Ararar")
    if "T" in x:
        try:
            spoyifyObj.start_playback(device['id'], None, [track], None, pos)
        except:
            print("plase check you're connected to the internet and spotify is open on the device")
            time.sleep(5)
            play()
    else:
        try:
            spoyifyObj.start_playback(device['id'], None, trackurl)
        except:
            print("plase check you're connected to the internet and spotify is open on the device")
            time.sleep(5)
            play()

if "T" in x:
    track = clientSocket.recv(69).decode('UTF8')
    pos = clientSocket.recv(bsize).decode('UTF8')
    print(track +" "+pos)
    print("welcome to the room " + displayName)
    play()
    while(isPlaying()==False):
        pass
else:
    print("welcome to the room,youre the first visitor")
    clientSocket.send("song is done".encode())
    trackurl = []
    trackurl.append(clientSocket.recv(bsize).decode('UTF8'))
    play()
    while(isPlaying()==False):
        pass
while (True):

    print("if you'd like to add a song, or to play next song press esc!")
    while isPlaying()!=False:
        try:
            data = ""
            data = clientSocket.recv(bsize)
            data = data.decode('UTF8')
            if data:
                print(data)
                if data[0:4] == "next":
                    track = data[5:41]
                    pos=data[42:]
                    if pos =="":
                        spoyifyObj.start_playback(device['id'], None, [track])
                    else:
                        spoyifyObj.start_playback(device['id'], None, [track],None,pos)
                    while (isPlaying() == False):
                        pass
                    print("if you'd like to add a song, or to play next song press esc!")

        except:
            pass

        if keyboard.is_pressed("esc"):
            response = input("1.add a song to the list\n2.play next song\nanswer: ")
            if response == "1":
                artistName = input("enter an artist name ")
                results = spoyifyObj.search(artistName, 1, 0, "artist")
                artist = results['artists']['items'][0]
                print(artist['name'] + " has " + str(artist['followers']['total']) + " followers , and his genre is " +
                      artist['genres'][0])
                webbrowser.open(artist['images'][0]['url'])
                artistId = artist["id"]
                trackUri = []
                trackArt = []
                z = 1
                albums = spoyifyObj.artist_albums(artistId)
                albums = albums['items']
                for item in albums:
                    print("album : " + item['name'])
                    albumId = item['id']
                    albumArt = item['images'][0]['url']
                    trackResults = spoyifyObj.album_tracks(albumId)
                    trackResults = trackResults['items']
                    for item in trackResults:
                        print(str(z) + ": " + item['name'])
                        trackUri.append(item['uri'])
                        trackArt.append(albumArt)
                        z = z + 1
                    print()
                songSelection = input("enter song to add to Queue: ")
                try:
                    clientSocket.send(trackUri[int(songSelection) - 1].encode())
                    print(clientSocket.recv(55).decode())
                    print("if you'd like to add a song, or to play next song press esc!")
                except:
                    print("Ivalid song number")
                    print("if you'd like to retry press esc!")
            if response == "2":
                print("2")
                clientSocket.send("play next song".encode())
    clientSocket.send("song is done".encode())
    track = clientSocket.recv(bsize).decode()
    if "!" in track:
        track = track[0:36]
        pos = track[38:]
        spoyifyObj.start_playback(device['id'], None, [track],None,pos)
    else:
        spoyifyObj.start_playback(device['id'], None, [track])
    while(isPlaying()==False):
        pass

# clientSocket.send(str(i).encode())
# data = clientSocket.recv(bsize)
# data=data.decode('utf8')
