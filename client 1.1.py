import socket

__author__ = 'rom gvili'

import webbrowser
import spotipy
import os
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import json
import keyboard
import time
from json.decoder import JSONDecodeError


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
client_credentials_manager = SpotifyClientCredentials('221e9a5fac5c4f40bb2de9c33ce7a863',
                                                      '8c5e85b7165840bbb605b43924952889')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
name = input("enter username ")


def addToQueue():
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
    clientSocket.send(trackUri[int(songSelection) - 1].encode())
    print(clientSocket.recv(bsize).decode())
    return


try:
    token = util.prompt_for_user_token(name, scope,
                                       client_id='221e9a5fac5c4f40bb2de9c33ce7a863',
                                       client_secret='8c5e85b7165840bbb605b43924952889',
                                       redirect_uri='http://google.com/')
except:
    os.remove(f".cache-{name}")
    token = util.prompt_for_user_token(name, scope,
                                       client_id='221e9a5fac5c4f40bb2de9c33ce7a863',
                                       client_secret='8c5e85b7165840bbb605b43924952889',
                                       redirect_uri='http://google.com/')
spoyifyObj = spotipy.Spotify(auth=token)
user = spoyifyObj.current_user()

print("your devices:\n")
devices = spoyifyObj.devices()
devices = devices['devices']
for device in devices:
    print(device['name'])
name = input("enter device name ")
for devic in devices:
    if devic['name'] == name:
        device = devic
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
    print("x")
while (True):
    time.sleep(5)
    print("if you'd like to add a song press esc!")
    while int(spoyifyObj.current_user_playing_track()['progress_ms']) <= int(
            spoyifyObj.current_user_playing_track()['item']['duration_ms']) - 3000:
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
            clientSocket.send(trackUri[int(songSelection) - 1].encode())
            print(clientSocket.recv(bsize).decode())
            print("if you'd like to add a song press esc!")
    clientSocket.send("song is done".encode())
    track = clientSocket.recv(bsize).decode()
    if "!" in track:
        track = track[:-1]
        spoyifyObj.start_playback(device['id'], None, [track],None,200)
    spoyifyObj.start_playback(device['id'], None, [track])
    time.sleep(2)

# clientSocket.send(str(i).encode())
# data = clientSocket.recv(bsize)
# data=data.decode('utf8')
