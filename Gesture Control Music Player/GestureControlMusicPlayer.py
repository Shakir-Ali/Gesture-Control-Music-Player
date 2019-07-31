## Single Palm >>> Play The Music
## Single Fist >>> Pause The Music
## One Palm and One Fist >>> Stop the Music
## Two Fists >>> Change the song in 2 seconds (Random)

import cv2
import vlc
import os
import time
import random as rd

path = input(r"Enter the full Path of the file which holds songs ")
songs = os.listdir(path)
songvalue=0
playsong = path+'\\'+songs[songvalue]
p=vlc.MediaPlayer(playsong)

v=cv2.VideoCapture(0)
face=cv2.CascadeClassifier(r"haarcascade_frontalface_alt2.xml")
palm=cv2.CascadeClassifier(r"palm.xml")
fist=cv2.CascadeClassifier(r"fist.xml")
flag=0
length = 0
volume = 0

def get_volume(length):
    length = length*13
    volume = length/25
    if volume > 100:
        volume = 100
    return volume

def next_song():
    global songvalue , playsong
    songvalue = rd.randint(0,len(songs))
    playsong = path+'\\'+songs[songvalue]
    
while(True):
    ret,i=v.read()
    faces=[]
    j=cv2.cvtColor(i,cv2.COLOR_BGR2GRAY)
    faces=face.detectMultiScale(j)
    f=fist.detectMultiScale(j)
    pl=palm.detectMultiScale(j)
    #print('palm',pl)
    #print('fist',f)
    for(x,y,w,h) in faces:
        cv2.rectangle(i,(x,y),(x+w,y+h),(255,0,0),5)
    for(x,y,w,h) in pl:
        cv2.rectangle(i,(x,y),(x+w,y+h),(0,255,0),5)
    for(x,y,w,h) in f:
        cv2.rectangle(i,(x,y),(x+w,y+h),(255,255,0),5)
    cv2.imshow('image',i)
    if len(pl)==1 and len(f)==0:
        p.play()
        flag = 1
    elif len(f)==1 and len(pl)==0: 
        p.pause()
        flag = 0
    elif len(f)==1 and len(pl)==1:
        p.stop()
        flag = 0
        
    if len(f)==2 and flag == 1:
        p.stop()
        time.sleep(2)
        next_song()
        print("Next Song Updated to Number",songvalue)
        p=vlc.MediaPlayer(playsong)
        p.play()
    
    '''if len(faces)>=1 and flag ==1:
        length = faces[0][2]
        volume = get_volume(length)
        volume = int(volume)
        p.audio_set_volume(volume)
    '''   
    k=cv2.waitKey(5)
    if(k==ord('q')):
        p.stop()
        cv2.destroyAllWindows()
        v.release()
        break
    elif(k==ord('v')):
        if len(pl)>=1 and len(f)==0:
            length = pl[0][2]
            volume = get_volume(length)
            volume = int(volume)
            p.audio_set_volume(volume)
    elif(k==ord('n')):
        p.stop()
        next_song()
        p=vlc.MediaPlayer(playsong)
        p.play()
