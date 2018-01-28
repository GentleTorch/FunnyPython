import numpy as np
import wave,math
import random
from collections import deque
import pygame
import sys,os
import time,argparse
from matplotlib import pyplot as plt

gShowPlot=False

pmNotes={'C4':262,'Eb':311,'F':349,'G':391,'Bb':466}



sRate=44100
nSample=sRate*5
x=np.arange(nSample)/float(sRate)
vals=np.sin(2.0*math.pi*220*x)

data=np.array(vals*32767,'int16').tostring()
file=wave.open('sine220.wav','wb')

file.setparams((1,2,sRate,nSample,'NONE','uncompressed'))
file.writeframes(data)
file.close()


def generateNote(freq):
    nSamples=44100
    sampleRate=44100
    N=int(sampleRate/freq)

    buf=deque([random.random()-0.5 for i in range(N)])
    if gShowPlot:
        axline,=plt.plot(buf)

    samples=np.array([0]*nSamples,'float32')
    for i in range(nSamples):
        samples[i]=buf[0]
        avg=0.996*0.5*(buf[0]+buf[1])
        buf.append(avg)
        buf.popleft()

        if gShowPlot:
            if i%1000==0:
                axline.set_ydata(buf)
                plt.draw()

    samples=np.array(samples*32767,'int16')
    return samples.tostring()

def writeWAVE(fname,data):
    file=wave.open(fname,'wb')
    nChannels=1
    sampleWidth=2
    frameRate=44100
    nFrames=44100
    file.setparams((nChannels,sampleWidth,frameRate,nFrames,'NONE','noncompressed'))
    file.writeframes(data)

    file.close()

class NotePlayer:
    def __init__(self):
        pygame.mixer.pre_init(44100,-16,1,2048)
        pygame.init()
        self.notes={}

    def add(self,fileName):
        self.notes[fileName]=pygame.mixer.Sound(fileName)

    def play(self,fileName):
        try:
            self.notes[fileName].play()
        except:
            print fileName+' Not Found!'

    def playRandom(self):
        index=random.randint(0,len(self.notes)-1)
        note=list(self.notes.values())[index]
        note.play()


def main():
    global gShowPlot

    parser=argparse.ArgumentParser(description='Generating sounds with Karplus String Algorithm')
    parser.add_argument('--display',action='store_true',required=False)
    parser.add_argument('--play',action='store_true',required=False)
    parser.add_argument('--piano',action='store_true',required=False)
    args=parser.parse_args()

    if args.display:
        gShowPlot=True
        plt.ion()

    nplayer=NotePlayer()
    print 'Creating Notes....'
    for name,freq in pmNotes.items():
        fileName=name+'.wav'
        if not os.path.exists(fileName) or args.display:
            data=generateNote(freq)
            print 'Creating '+fileName+'...'
            writeWAVE(fileName,data)
        else:
            print fileName+' already created. Skipping...'

        nplayer.add(fileName)
        if args.display:
            nplayer.play(fileName)
            time.sleep(0.5)

    if args.play:
        i=0;
        while i<10000:
            try:
                nplayer.playRandom()
                rest=np.random.choice([1,2,4,8],1,p=[0.15,0.7,0.1,0.05])
                time.sleep(0.25*rest[0])
            except KeyboardInterrupt:
                exit()
            i+=1

    if args.piano:
        while True:
            for event in pygame.event.get():
                if event.type==pygame.KEYUP:
                    print 'key pressed'
                    nplayer.playRandom()
                    time.sleep(0.5)


if __name__=='__main__':
    main()



