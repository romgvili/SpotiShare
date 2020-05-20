__author__ = 'rom gvili'
import win32clipboard
import pygame as pg
import socket
import spotipy
from os import path
import os
import spotipy.util as util
import sys
import numpy as np
import time
import io
import urllib.request
from PIL import Image
from resizeimage import resizeimage
def current_milli_time():
    return int(round(time.time() * 1000))
def resource_path(relative_path):
    try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def levenshtein(seq1, seq2):
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = np.zeros ((size_x, size_y))
    for x in range(size_x):
        matrix [x, 0] = x
    for y in range(size_y):
        matrix [0, y] = y

    for x in range(1, size_x):
        for y in range(1, size_y):
            if seq1[x-1] == seq2[y-1]:
                matrix [x,y] = min(
                    matrix[x-1, y] + 1,
                    matrix[x-1, y-1],
                    matrix[x, y-1] + 1
                )
            else:
                matrix [x,y] = min(
                    matrix[x-1,y] + 1,
                    matrix[x-1,y-1] + 1,
                    matrix[x,y-1] + 1
                )
    return (matrix[size_x - 1, size_y - 1])


def main():

    trackLists = []
    heb = 'אבגדהוזחטיכלמנסעפצקרשתץףך'
    address = '127.0.0.1'
    port = 8000
    bsize = 1024
    scope = 'playlist-modify-public streaming user-modify-playback-state user-read-playback-state user-read-currently-playing'
    screen = pg.display.set_mode((640, 480))
    pg.display.set_caption('SPOTISHARE by Rom Gvili')
    startscreen = pg.image.load("C:/Users/rom/PycharmProjects/top5/graphics/start.png")
    font = pg.font.Font(None, 32)
    clock = pg.time.Clock()
    input_box = pg.Rect(224, 150, 140, 32)
    color_inactive = pg.Color('lightskyblue3')
    color_active = pg.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = 'enter username'
    done = False
    b = False
    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if input_box.collidepoint(event.pos):
                    # Toggle the active variable.
                    active = not active
                else:
                    active = False
                # Change the current color of the input box.
                color = color_active if active else color_inactive
            if event.type == pg.KEYDOWN:
                if active:
                    if event.key == pg.K_RETURN:
                        b = True
                    elif event.key == pg.K_BACKSPACE:
                        text = text[:-1]
                    elif event.key == pg.K_v and pg.key.get_mods() & pg.KMOD_CTRL:
                        win32clipboard.OpenClipboard()
                        text+= win32clipboard.GetClipboardData()

                    else:
                        text += event.unicode
        if b == True:
            break



        screen.blit(startscreen,(0,0))
        # Render the current text.
        txt_surface = font.render(text, True, color)
        # Resize the box if the text is too long.
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        # Blit the text.
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        # Blit the input_box rect.
        pg.draw.rect(screen, color, input_box, 2)

        pg.display.flip()
        clock.tick(30)
    name = text
    pg.display.quit()
    try:
        if path.exists(f".cache-{name}"):
            file = open(f".cache-{name}")
            text = file.read()
            text = text[270:401]
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
    pg.init()
    screen = pg.display.set_mode((640, 480))
    pg.display.set_caption('SPOTISHARE by Rom Gvili')
    devicesimg = pg.image.load("C:/Users/rom/PycharmProjects/top5/graphics/devices.png")
    font = pg.font.SysFont(None, 34)
    font2 = pg.font.SysFont(None, 20)
    fontheb = pg.font.SysFont('arial',20)
    clock = pg.time.Clock()
    input_box = pg.Rect(224, 150, 140, 32)
    color_inactive = pg.Color('lightskyblue3')
    color_active = pg.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = 'enter device'
    done = False
    global device
    devices = spoyifyObj.devices()
    devices = devices['devices']
    lis = "your devices: "
    for device in devices:
        lis += device['name'] + ", "
    LENG = len(devices)
    text = "enter the desired device"
    text2 = font2.render(lis, True,(0,255,0), (0,0,128))
    textRect2 = text2.get_rect()
    textRect2.center = (640 // 2, 480 // 2)
    screen.blit(text2, textRect2)
    b = False
    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if input_box.collidepoint(event.pos):
                    # Toggle the active variable.
                    active = not active
                else:
                    active = False
                # Change the current color of the input box.
                color = color_active if active else color_inactive
            if event.type == pg.KEYDOWN:
                if active:
                    if event.key == pg.K_RETURN:
                        b = True
                    elif event.key == pg.K_BACKSPACE:
                        text = text[:-1]
                    elif event.key == pg.K_v and pg.key.get_mods() & pg.KMOD_CTRL:
                        win32clipboard.OpenClipboard()
                        text += win32clipboard.GetClipboardData()
                    else:
                        text += event.unicode
        if b == True:
            break
        screen.blit(devicesimg, (0, 0))
        # Render the current text.
        txt_surface = font.render(text, True, color)
        for c in text:
            if c not in heb:
                txt_surface = font.render(text, True, color)
            else:
                txt_surface = fontheb.render(text[::-1], True, color)
                break

        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        # Blit the text.
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        # Blit the input_box rect.
        pg.draw.rect(screen, color, input_box, 2)
        text2 = font2.render(lis, True, (0, 255, 0), (0, 0, 128))
        textRect2 = text2.get_rect()
        textRect2.center = (640 // 2, 480 // 2)
        screen.blit(text2, textRect2)
        pg.display.flip()
        clock.tick(30)
    for d in devices:
        print(text)
        print(d['name'])
        if text == d['name']:
            print(text)
            device= d
            break
    print(device['name'])
    displayName = user['display_name']
    Followers = user['followers']['total']
    bg = pg.image.load("C:/Users/rom/PycharmProjects/top5/graphics/playing.png")
    screen.blit(bg,(0,0))
    text2 = font2.render("welcome to SpotiShare " + displayName+ "!", True, (0, 255, 0), (0, 0, 128))
    textRect2 = text2.get_rect()
    textRect2.center = (640 // 2, 480 // 2)
    screen.blit(text2, textRect2)
    text3 = font2.render("you have " + str(Followers)+ "followers!", True, (0, 255, 0), (0, 0, 128))
    textRect3 = text3.get_rect()
    textRect3.center = (640 // 2, (480 // 2)+20)
    screen.blit(text3, textRect3)
    pg.display.flip()
    time.sleep(2)
    clientSocket = socket.socket()
    clientSocket.connect((address, port))
    clientSocket.settimeout(2)
    print(clientSocket.recv(22).decode('UTF8'))
    x = clientSocket.recv(34).decode('UTF8')

    def play():
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
    def isPlaying():
        try:
            if spoyifyObj.currently_playing()["is_playing"]:
                return True
            return False
        except:
            return False
    if "T" in x:
        yo = pg.image.load("C:/Users/rom/PycharmProjects/top5/graphics/welcome.png")
        screen.blit(yo,(0,0))
        pg.display.flip()
        track = clientSocket.recv(69).decode('UTF8')
        pos = clientSocket.recv(bsize).decode('UTF8')
        play()
        while (isPlaying() == False):
            pass
    else:
        yo = pg.image.load("C:/Users/rom/PycharmProjects/top5/graphics/first.png")
        screen.blit(yo,(0,0))
        pg.display.flip()
        clientSocket.send("song is done".encode())
        trackurl = []
        trackurl.append(clientSocket.recv(bsize).decode('UTF8'))
        play()
        while (isPlaying() == False):
            pass
    time.sleep(5)
    yo = pg.image.load("C:/Users/rom/PycharmProjects/top5/graphics/last.png")
    screen.blit(yo,(0,0))
    addbutton = pg.Rect(500, 40, 100, 100)
    nextbutton = pg.Rect(500, 200, 100, 100)
    textbutton = pg.Rect(500, 360, 100, 100)
    nextbuttontext = font2.render("play next song", True, (0, 255, 0), (0, 0, 128))
    nextbuttonRect = nextbuttontext.get_rect()
    nextbuttonRect.center = (550, 250)
    screen.blit(nextbuttontext, nextbuttonRect)
    addbuttontext = font2.render("add", True, (0, 255, 0), (0, 0, 128))
    addbuttonRect = addbuttontext.get_rect()
    addbuttonRect.center = (550, 90)
    screen.blit(addbuttontext, addbuttonRect)
    def nextsongpressed():
        clientSocket.send("play next song".encode())
    def addsongpressed():
        color = color_inactive
        screen.blit(bg,(0,0))
        text = "enter artist name"
        txt_surface = font.render(text, True,color )
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pg.draw.rect(screen, color, input_box, 2)
        b=False
        active = False
        while not done:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    # If the user clicked on the input_box rect.
                    if input_box.collidepoint(event.pos):
                        # Toggle the active variable.
                        active = not active
                    else:
                        active = False
                    # Change the current color of the input box.
                    color = color_active if active else color_inactive
                if event.type == pg.KEYDOWN:
                    if active:
                        if event.key == pg.K_RETURN:
                            b = True
                        elif event.key == pg.K_BACKSPACE:
                            text = text[:-1]
                        elif event.key == pg.K_v and pg.key.get_mods() & pg.KMOD_CTRL:
                            win32clipboard.OpenClipboard()
                            text += win32clipboard.GetClipboardData()
                        else:
                            text += event.unicode
            screen.blit(bg,(0,0))
            txt_surface = font.render(text, True, color)
            for c in text:
                if c not in heb:
                    txt_surface = font.render(text, True, color)
                else:
                    txt_surface = fontheb.render(text[::-1], True, color)
                    break
            width = max(200, txt_surface.get_width() + 10)
            input_box.w = width
            screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
            pg.draw.rect(screen, color, input_box, 2)
            pg.display.flip()
            if b == True:
                break
        artistName = text
        results = spoyifyObj.search(artistName, 1, 0, "artist")
        try:
            artist = results['artists']['items'][0]
        except:
            screen.blit(bg,(0,0))
            text = "artist wasnt found"
            txt_surface = font.render(text, True, color)
            width = max(200, txt_surface.get_width() + 10)
            input_box.w = width
            screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
            pg.draw.rect(screen, color, input_box, 2)
            pg.display.flip()
            time.sleep(3)
            screen.blit(yo, (0, 0))
            return
        #print(artist['name'] + " has " + str(artist['followers']['total']) + " followers , and his genre is " + artist['genres'][0])
        urllib.request.urlretrieve(artist['images'][0]['url'],'pic.png')
        with open('pic.png', 'r+b') as f:
            with Image.open(f) as image:
                artistpic = resizeimage.resize_cover(image, [640, 480])
                artistpic.save('pic.png', image.format)
        artistpic = pg.image.load('pic.png')
        screen.blit(artistpic,(0,0))
        pg.display.flip()
        text = "enter song name"
        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pg.draw.rect(screen, color, input_box, 2)
        b=False
        active = False
        while not done:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    # If the user clicked on the input_box rect.
                    if input_box.collidepoint(event.pos):
                        # Toggle the active variable.
                        active = not active
                    else:
                        active = False
                    # Change the current color of the input box.
                    color = color_active if active else color_inactive
                if event.type == pg.KEYDOWN:
                    if active:
                        if event.key == pg.K_RETURN:
                            b = True
                        elif event.key == pg.K_BACKSPACE:
                            text = text[:-1]
                        elif event.key == pg.K_v and pg.key.get_mods() & pg.KMOD_CTRL:
                            win32clipboard.OpenClipboard()
                            text += win32clipboard.GetClipboardData()
                        else:
                            text += event.unicode
            screen.blit(artistpic, (0, 0))
            txt_surface = font.render(text, True, color)
            for c in text:
                if c not in heb:
                    txt_surface = font.render(text, True, color)
                else:
                    txt_surface = fontheb.render(text[::-1], True, color)
                    break
            width = max(200, txt_surface.get_width() + 10)
            input_box.w = width
            screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
            pg.draw.rect(screen, color, input_box, 2)
            pg.display.flip()
            if b == True:
                break
        songname = text.upper()

        artistId = artist["id"]
        albums = {}
        count = 0
        while len(albums) % 10 == 0:
            albums.update(spoyifyObj.artist_albums(artistId, None, None, 20,count))
            count += 20
        albums = spoyifyObj.artist_albums(artistId,None,None,50)
        print(albums)
        albums = albums['items']
        close = []
        closeuri=[]
        albumsi = []
        names ={}
        def checker(na , di, al):
            if na in di:
                if di[na] == al:
                    return False
            return True
        for album in albums:
            albumId = album['id']
            trackResults = spoyifyObj.album_tracks(albumId)
            trackResults = trackResults['items']
            for item in trackResults:
                if (songname in item['name'].upper() or songname == item['name'].upper()or levenshtein(songname,item['name'].upper())<4.0) and item['uri'] not in closeuri and checker(item['name'].upper(),names,album['name']):
                    close.append(item)
                    closeuri.append(item['uri'])
                    albumsi.append(album['name'])
                    names[item['name'].upper()] = album['name']
        if len(close)!=0:
            closest = ""
            mini = 5
            if len(close)>1:
                count = 1
                for ite in close:
                    text4 = font2.render(str(count) + ". " + ite['name'] + " from " + albumsi[count-1], True, (0, 255, 0),(0, 0, 128))
                    textRect4 = text4.get_rect()
                    textRect4.center = (640 // 2, (480 // 2)+count*15)
                    screen.blit(text4, textRect4)
                    count+=1
                pg.display.flip()
                text = "enter song number"
                txt_surface = font.render(text, True, color)
                width = max(200, txt_surface.get_width() + 10)
                input_box.w = width
                screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
                pg.draw.rect(screen, color, input_box, 2)
                b = False
                active = False
                while not done:
                    for event in pg.event.get():
                        if event.type == pg.QUIT:
                            pg.quit()
                        if event.type == pg.MOUSEBUTTONDOWN:
                            # If the user clicked on the input_box rect.
                            if input_box.collidepoint(event.pos):
                                # Toggle the active variable.
                                active = not active
                            else:
                                active = False
                            # Change the current color of the input box.
                            color = color_active if active else color_inactive
                        if event.type == pg.KEYDOWN:
                            if event.key == pg.K_RETURN:
                                b = True
                            if active:
                                if event.key == pg.K_RETURN:
                                    b = True
                                elif event.key == pg.K_BACKSPACE:
                                    text = text[:-1]
                                elif event.key == pg.K_v and pg.key.get_mods() & pg.KMOD_CTRL:
                                    win32clipboard.OpenClipboard()
                                    text += win32clipboard.GetClipboardData()
                                else:
                                    text += event.unicode
                    screen.blit(artistpic, (0, 0))
                    txt_surface = font.render(text, True, color)
                    for c in text:
                        if c not in heb:
                            txt_surface = font.render(text, True, color)
                        else:
                            txt_surface = fontheb.render(text[::-1], True, color)
                            break
                    width = max(200, txt_surface.get_width() + 10)
                    input_box.w = width
                    screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
                    pg.draw.rect(screen, color, input_box, 2)
                    count=1
                    for ite in close:
                        text4 = font2.render(str(count) + ". " + ite['name'] + " from " + albumsi[count-1],True, (0, 255, 0), (0, 0, 128))
                        textRect4 = text4.get_rect()
                        textRect4.center = (640 // 2, (480 // 2) + count * 15)
                        screen.blit(text4, textRect4)
                        count += 1
                    pg.display.flip()
                    if b == True:
                        break
                closest = close[int(text)-1]['uri']
            else:
                closest= close[0]['uri']
            clientSocket.send(closest.encode())
            print(clientSocket.recv(55).decode())
            screen.blit(yo, (0, 0))
            return
        screen.blit(yo, (0, 0))
        screen.blit(artistpic, (0, 0))
        text = "song wasnt found"
        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pg.draw.rect(screen, color, input_box, 2)
        pg.display.flip()
        time.sleep(3)
        screen.blit(yo, (0, 0))
        return
    while True:
        while isPlaying() != False:
            try:
                data = ""
                data = clientSocket.recv(bsize)
                data = data.decode('UTF8')
                if data:
                    if data[0:4] == "next":
                        track = data[5:41]
                        pos = data[42:]
                        if pos == "":
                            spoyifyObj.start_playback(device['id'], None, [track])
                        else:
                            spoyifyObj.start_playback(device['id'], None, [track], None, pos)
                        while (isPlaying() == False):
                            pass

            except:
                pass
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos  # gets mouse position
                    if nextbutton.collidepoint(mouse_pos):
                        nextsongpressed()
                    if addbutton.collidepoint(mouse_pos):
                        addsongpressed()
            pg.draw.rect(screen, [255, 0, 0], addbutton)  # draw button
            pg.draw.rect(screen, [255, 0, 0], nextbutton)  # draw button
            pg.draw.rect(screen, [255, 0, 0], textbutton)  # draw button
            screen.blit(nextbuttontext, nextbuttonRect)
            screen.blit(addbuttontext, addbuttonRect)
            pg.display.update()
        if spoyifyObj.currently_playing()["progress_ms"]==0:
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
        else:
            spoyifyObj.start_playback(device['id'], None, [track], None,spoyifyObj.currently_playing()["progress_ms"]+1000 )


if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()