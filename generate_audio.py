from pydub import AudioSegment
from random import randint, choice, random

## a so-called "shit-script" if you will

## basically アルスの草畑.py but the audio is compiled

# parameters
file_path = "output/"
file_name = "Ars laughs for 10 minutes"
file_type = "mp3"

########## min # s  #  ms  #
duration = 10  * 60 * 1000 # approximation
bgm_start = 0 # ms
bgm_file = "audio/bgm_maoudamashii_acoustic32.mp3"
first_laugh = 100 # ms
end_max_silence = 1000 # ms, longest allowed time after last laugh

bgm_on = True
laugh_variations = 27
wheeze_variations = 3
wheeze_prob = 0.05 # instead of laugh
wheeze_cooldown = 3 # at least x laughs between each wheeze
prevs_size = 3 # the same variation can only be played every nth time
laugh_inhale_prob = 0.2
wheeze_inhale_prob = 0.8
inhale_range = (2,5) # at least x laughs between each inhale but no more than y

########################################

def subset(a,b): # is every element in a also in b?
    return all(map(lambda elem: elem in b, a))

laugh_count = [0] * laugh_variations
wheeze_count = [0] * wheeze_variations
laugh_inhale_count = laugh_count.copy()
wheeze_inhale_count = wheeze_count.copy()

time = 0
base = None
if bgm_on:
    base = AudioSegment.silent(bgm_start)
    bgm = AudioSegment.from_mp3(bgm_file) - 30
    # extend bgm
    while len(base) < duration:
        base = base.append(bgm,crossfade=0)
else:
    base = AudioSegment.silent(duration)

base = base.append(AudioSegment.silent(first_laugh),crossfade=0)

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
        
longest_laugh_time = max(map(lambda s1,s2: len(s1)+len(s2),laughs,laugh_inhales))
longest_wheeze_time = max(map(lambda s1,s2: len(s1)+len(s2),wheezes,wheeze_inhales))


prevs = [-1] * prevs_size
wheeze_counter = 0
inhale_counter = 0
i = 0
    
while time + longest_laugh_time < duration:
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
        occurence_count = laugh_count
        occurence_inhale_count = laugh_inhale_count
    else:
        laugh_selection = wheezes
        inhale_selection = wheeze_inhales
        inhale_prob = wheeze_inhale_prob
        occurence_count = wheeze_count
        occurence_inhale_count = wheeze_inhale_count
        
    laugh = choice([laugh for laugh in laugh_selection if laugh not in prevs])
    laugh_index = laugh_selection.index(laugh)  
    print("{} #{} ".format(laugh_type,laugh_index+1),end="")
    
    prevs[i] = laugh
    i = (i+1) % prevs_size
    occurence_count[laugh_index] += 1

    base = base.overlay(laugh_selection[laugh_index],position=time)
    time += len(laugh_selection[laugh_index])

# occasional inhales for more realism
    if ((random() < inhale_prob and inhale_counter >= inhale_range[0])
            or inhale_counter > inhale_range[1]):
        inhale_counter = 0
        print("*inhale*")
        occurence_inhale_count[laugh_index] += 1
        base = base.overlay(inhale_selection[laugh_index],position=time)
        time += len(inhale_selection[laugh_index])
    else:
        inhale_counter += 1
        print()
        time += randint(300,500)


# truncate excess bgm
if duration - time < end_max_silence:
    base = base[:duration]
else:
    base = base[:time+end_max_silence]

print("Exporting...")
base.export(file_path + file_name + "." + file_type, format=file_type)
print("Done!")


# statistics
total_laughs = sum(laugh_count)
total_wheezes = sum(wheeze_count)
total_laugh_inhales = sum(laugh_inhale_count)
total_wheeze_inhales = sum(wheeze_inhale_count)
print("\nStatistics:\n")
print("{} laughs ({}% of total), {} inhales ({}% of total)".format(
    total_laughs, round(100 * total_laughs / (total_laughs + total_wheezes),2),
    total_laugh_inhales, round(100 * total_laugh_inhales / (total_laugh_inhales + total_wheeze_inhales),2)
    ))
print("{} wheezes ({}% of total), {} inhales ({}% of total)".format(
    total_wheezes, round(100 * total_wheezes / (total_laughs + total_wheezes),2),
    total_wheeze_inhales, round(100 * total_wheeze_inhales / (total_laugh_inhales + total_wheeze_inhales),2)
    ))
print("Laughs by variation:")
for i in range(laugh_variations):
    print("{}: {} ({}%)".format(i+1, laugh_count[i], round(100 * laugh_count[i] / total_laughs,2)))
print("Laugh-inhales by variation:")
for i in range(laugh_variations):
    print("{}: {} ({}%)".format(i+1, laugh_inhale_count[i], round(100 * laugh_inhale_count[i] / total_laugh_inhales,2)))
print("Wheezes by variation:")
for i in range(wheeze_variations):
    print("{}: {} ({}%)".format(i+1, laugh_count[i], round(100 * wheeze_count[i] / total_wheezes,2)))
print("Wheeze-inhales by variation:")
for i in range(wheeze_variations):
    print("{}: {} ({}%)".format(i+1, wheeze_inhale_count[i], round(100 * wheeze_inhale_count[i] / total_wheeze_inhales,2)))

