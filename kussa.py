#coding: utf-8
import spidev
import RPi.GPIO as GPIO
import time
import threading

from pydub import AudioSegment
from pydub.playback import play

def setup_spi():
    spi = spidev.SpiDev()
    spi.open(0, 0)
    spi.max_speed_hz = 1000000
    spi.bits_per_word = 8
    return spi

def measure(spi, ch):
    start = 0x47
    sgl = 0x20
    msbf = 0x08
    dummy = 0xff
    ad = spi.xfer2([(start + sgl + ch + msbf), dummy])
    val = ((ad[0] & 0x03) << 8) + ad[1]
    return val

def play_sound(wav_file):
    play(wav_file)

def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.OUT)
    GPIO.setup(22, GPIO.OUT)

    spi = setup_spi()

    threshold = 600

    wav_file = AudioSegment.from_file("kuse1.wav", format="wav")

    try:
        while True:
            time.sleep(0.237)
            
            GPIO.output(22, True)
            time.sleep(0.003)

            ch0_val = measure(spi, 0)
            Val = 1023 - ch0_val
            time.sleep(0.002)
            GPIO.output(22, False)
            
            GPIO.output(17, True)
            time.sleep(0.008)
            GPIO.output(17, False)
            
            print(Val)

            if Val > threshold:
                print("くっさ！！")
                sound_thread = threading.Thread(target=play_sound, args=(wav_file,))
                sound_thread.start()
                
    except KeyboardInterrupt:
        pass

    spi.close()
    GPIO.cleanup()

if __name__ == "__main__":
    main()
