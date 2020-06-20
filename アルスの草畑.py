from pydub import AudioSegment
from pydub.playback import play
from time import sleep
from random import randint, choice, random
from threading import Thread
from sys import stdout

## a so-called "shit-script" if you will

## endlessly plays random Ars laughs based on samples in the 'audio' folder

# parameters
bgm_on = False#True
laugh_variations = 27
wheeze_variations = 3
wheeze_prob = 0.05 # instead of laugh
wheeze_cooldown = 3 # at least x laughs between each wheeze
prevs_size = 3 # ensure variety of laughs
laugh_inhale_prob = 0.2
wheeze_inhale_prob = 0.8
inhale_range = (2,5) # at least x laughs between each but no more than y
########################################

def subset(a,b): # is every element in a also in b?
    return all(map(lambda elem: elem in b, a))

def laugh_thread():
    laughs = []
    laugh_inhales = []
    wheezes = []
    wheeze_inhales = []
    for i in range(1,laugh_variations+1):
        laughs.append(AudioSegment.from_wav("audio/laugh #{}.wav".format(i)))
        laugh_inhales.append(AudioSegment.from_wav("audio/laugh_inhale #{}.wav".format(i)))
    for i in range(1,wheeze_variations+1):
        wheezes.append(AudioSegment.from_wav("audio/wheeze #{}.wav".format(i)))
        wheeze_inhales.append(AudioSegment.from_wav("audio/wheeze_inhale #{}.wav".format(i)))
    
    prevs = [-1] * prevs_size
    wheeze_counter = 0
    inhale_counter = 0
    i = 0
    
    while True:
        if (random() < wheeze_prob and not subset(wheezes,prevs) and wheeze_counter >= wheeze_cooldown):
            laugh_type = "wheeze"
            wheeze_counter = 0
        else:
            laugh_type = "laugh"
            wheeze_counter += 1
        
        if laugh_type == "laugh":
            laugh_selection = laughs
            inhale_selection = laugh_inhales
            inhale_prob = laugh_inhale_prob
        else:
            laugh_selection = wheezes
            inhale_selection = wheeze_inhales
            inhale_prob = wheeze_inhale_prob
            
        laugh = choice([laugh for laugh in laugh_selection if laugh not in prevs])
        laugh_index = laugh_selection.index(laugh)  
        print("{} #{} ".format(laugh_type,laugh_index+1),end="")
            
        prevs[i] = laugh
        i = (i+1) % prevs_size
        
        stdout.flush() # print won't display until after the thread's finished otherwise
        play(laugh)

        # occasional inhales for more realism
        if ((random() < inhale_prob and inhale_counter >= inhale_range[0])
                or inhale_counter > inhale_range[1]):
            inhale_counter = 0
            print("*inhale*")
            play(inhale_selection[laugh_index])
        else:
            inhale_counter += 1
            print()
            sleep(randint(3,5)/10)
            
def bgm_thread():
    bgm = AudioSegment.from_mp3("audio/bgm_maoudamashii_acoustic32.mp3") - 30
    while True:
        play(bgm)


# main start
if bgm_on:
    Thread(target=bgm_thread).start()
Thread(target=laugh_thread).start()
