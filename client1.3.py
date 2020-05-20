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
    try:
        if path.exists(f".cache-{name}"):
            file = open(f".cache-{name}")
            text = file.read()
            text= text[270:401]
            token = spotipy.SpotifyOAuth.refresh_access_token(text)

    except:
        token = util.prompt_for_user_token(name, scope,
                                           client_id='221e9a5fac5c4f40bb2de9c33ce7a863',
                                           client_secret='8c5e85b7165840bbb605b43924952889',
                                           redirect_uri='http://google.com/')
except ConnectionError:
    webbrowser.open('https://imgur.com/a/zZ3OW0f')
    sys.exit()
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
print(clientSocket.recv(bsize).decode('UTF8'))
x = clientSocket.recv(34).decode('UTF8')

print(x)
if "T" in x:
    track = clientSocket.recv(69).decode('UTF8')
    pos = clientSocket.recv(bsize).decode('UTF8')
    print(track)
    print(pos)
    spoyifyObj.start_playback(device['id'], None, [track], None,current_milli_time()-int(pos)+200)
    print("welcome to the room " + displayName)
else:
    print("welcome to the room,youre the first visitor")
    clientSocket.send("song is done".encode())
    trackurl = []
    trackurl.append(clientSocket.recv(bsize).decode('UTF8'))
    print(trackurl)
    spoyifyObj.start_playback(device['id'], None, trackurl)
    while(isPlaying()==False):
        pass
    print("x")
while (True):
    time.sleep(5)
    print("if you'd like to add a song press esc!")
    while isPlaying()!=False:
        if keyboard.is_pressed("esc"):
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
            songSelection = input("enter song to add to Queue")
            try:
                clientSocket.send(trackUri[int(songSelection) - 1].encode())
                print(clientSocket.recv(bsize).decode())
                print("if you'd like to add a song press esc!")
            except:
                print("Ivalid song number")
                print("if you'd like to retry press esc!")
    print("a")
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
