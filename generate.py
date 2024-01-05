import pickle
import math


amplitude_Мах = 0xFFFF - 0xFFFF / 10
amplitude_Мin = 0xFFFF / 10


#Частота семплирования
f_samples = 44100.0

f_Мах = 5000.0
f_Мin = 300.0

old_data = f_Мin
new_data = f_Мin


F0 = (f_Мах + f_Мin) / 2.0

Fb = (f_Мах - f_Мin) / 10.0

#Частота сигнала [f_Мin, f_Мах - Fb]
# value = [0, 9]
def get_freq(value):
    if value in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F' ):
        return f_Мin + Fb * float(int('0x0'+value, 16))
    else:
        return f_Мin

#делитель длительности сигнала в 1 секунду
freq_divider = 10

count = int(f_samples / freq_divider)

amplitude_start = 0xFFFF / 2
counter = 0


# начальная фаза
FI0 = 0


def FI(value):
    return math.pi * (F0 * value / count + Fb / 2 * value * value / count /count)


def new_data_function(new_value_line):
    global old_data
    global new_data
    global counter

    pi = math.pi
    array = []
    for new_value in new_value_line[:]:

        counter += 1
        old_data = new_data
        new_data = float(get_freq(new_value))
        print("Note:", new_data)
        for i in range(1, count+2):
            # value_0_9 = float(old_data) + (float(new_data) - float(old_data)) * (float(i) / count)
            # x = (2.0 * pi * float(i) / count) * (1.0 + 1.0 * (value_0_9) / 10.0)
            # amplitude_ = 256.0 * (1.0 + math.sin(x))

            f_value_0_9 = float(old_data) + ((float(new_data) - float(old_data)) * float(i) / count)
            fi = FI(f_value_0_9)

            # amplitude_ = 256.0 * (1.0 + math.sin(x))
            amplitude_ = 256.0 * (1.0 - math.cos(fi))
            array.append(int(amplitude_) & 0xFF)

    with open("out.wav", "ab") as mypicklefile:
        pickle.dump(array, mypicklefile)


with open('out.txt') as f:
    [new_data_function(line) for line in f.readlines()]

print("Всего: ", counter)
# amplitude_( вычисляемая ) = amplitude_( start ) * ((amplitude_(Мах) - amplitude_(Мin)) / 0xFFFF) * sin ( )

# x    - [0-8000]
# 2*pi - 8000

# x = (2*pi*[0-8000]/8000)

# full_len = |B - A| // длина вектора, соединяющего две точки == длина отрезка
# C = A + (B - A) * (len / full_len)

# C = A + (B - A) * (len / full_len)
