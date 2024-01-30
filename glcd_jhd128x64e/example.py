import jhd_glcd  # glcd_jhd128x64e
import time
import numpy as np
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)  # Use BCM GPIO numbers

state = 0  # menu screen
cursor = 0
GLCD = jhd_glcd.KS0108(rs=3, en=7, d0=12, d1=16, 
                              d2=26, d3=14, d4=15, d5=2, 
                              d6=18, d7=25, chip_set0=22, 
                              chip_set1=23, reset=24)

BUTTON_ONE = 13
BUTTON_TWO = 27
BUTTON_THREE = 17


def print_menu(choice):
    global GLCD
    GLCD.set_cursor(0,0,0)
    GLCD.print_str("Please choose a menu:\n\n")
    GLCD.print_str("# Show weapon list\n", choice == 0)
    GLCD.print_str("# Show all logs", choice == 1)

def weapon_list(l):
    print("shouldn't be here yet")
    # pass

def all_logs(l, chosen):
    global GLCD
    GLCD.clear()
    GLCD.set_cursor(0,0,0)
    GLCD.print_str('name room in  Time\n')
    start = 0
    GLCD.set_cursor(0,1,0)  # maybe can remove this line
    for idx, w in enumerate(l[start:start+6]):
        GLCD.print_str(f'{w[0]: <6} {w[1]: <5} {w[2]: <3} {w[3]}\n', idx==chosen if chosen <= 5 else idx==5)
        if idx==5:  # ran out of space
            GLCD.set_cursor(0,7,60)
            if start != (len(l) - 6):
                GLCD.print_chr(chr(0x7F))  # print down arrow
            else:
                GLCD.print_str('  ')
            break
    if user_input != 'exit':
        if user_input == 'u' and chosen < len(l) - 1:
            chosen += 1
            if chosen > 5:
                start += 1
        elif user_input == 'd' and chosen > 0:
            chosen -= 1
            if chosen >= 5:
                start -= 1


FUNC_LIST = [weapon_list, all_logs]

def up_press(channel):
    global GLCD
    global state
    global cursor
    if cursor > 0:
        cursor -= 1
    if state == 0:
        print_menu(0)

def down_press(channel):
    global state
    global cursor
    if state == 0:
        if cursor < 1:
            cursor += 1
        print_menu(1)
    elif state == 1:
        # all_logs(GLCD, l)
        state = 0

def select_press(channel):
    l = []
    for i in range(10):
        l.append([f'w{i}', f'lab{(i % 2) + 1}', i % 2, '12.1  11:25'])
    global state
    global cursor
    if state == 0:
        FUNC_LIST[cursor](l)
        state = cursor + 1


GPIO.setup(BUTTON_ONE, GPIO.IN)
GPIO.setup(BUTTON_TWO, GPIO.IN)
GPIO.setup(BUTTON_THREE, GPIO.IN)

GPIO.add_event_detect(BUTTON_ONE,GPIO.RISING,callback=up_press, bouncetime=250)
GPIO.add_event_detect(BUTTON_TWO,GPIO.RISING,callback=down_press, bouncetime=250)
GPIO.add_event_detect(BUTTON_THREE,GPIO.RISING,callback=select_press, bouncetime=250)


def main():
    global GLCD
    GLCD.start()
    print_menu(0)
    input()
    GLCD.clear()


if __name__ == "__main__":
    main()
