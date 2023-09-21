#coding: utf-8
import spidev
import RPi.GPIO as GPIO
import time

from pydub import AudioSegment
from pydub.playback import play

threshold = 600 #閾値を変えるときはここを変更

GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT)
GPIO.setup(22,GPIO.OUT)

spi = spidev.SpiDev()

spi.open(0,0)

spi.max_speed_hz=1000000

spi.bits_per_word=8

dummy = 0xff
start = 0x47
sgl = 0x20

ch0 = 0x00

msbf = 0x08

# read to mp3
wav_file = AudioSegment.from_file("kuse1.wav", format="wav")


def measure(ch):
    ad = spi.xfer2( [ (start + sgl + ch + msbf), dummy ] )
    val = ((ad[0] & 0x03) << 8) + ad[1]
    return val

try:
    while 1:
        time.sleep(0.237)
              
        GPIO.output(22,True)
        time.sleep(0.003)

        ch0_val = measure(ch0)
        Val = 1023 - ch0_val
        time.sleep(0.002)
        GPIO.output(22,False)
        
        GPIO.output(17,True)
        time.sleep(0.008)
        GPIO.output(17,False)
        
        print(Val)

        if Val > threshold:
            print("くっさ！！")
            play(wav_file)
           # pygame.mixer.music.play(0)
except KeyboardInterrupt:
    pass

spi.close()