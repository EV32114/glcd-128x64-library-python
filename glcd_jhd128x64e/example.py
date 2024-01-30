import jhd_glcd  # glcd_jhd128x64e
from enum import Enum
import RPi.GPIO as GPIO

# TODO remove later
ll = []
for i in range(10):
    ll.append([f'w{i}', f'lab{(i % 2) + 1}', i % 2, '12.1  11:25'])

GPIO.setmode(GPIO.BCM)  # Use BCM GPIO numbers

GLCD = jhd_glcd.KS0108(rs=3, en=7, d0=12, d1=16,
                       d2=26, d3=14, d4=15, d5=2,
                       d6=18, d7=25, chip_set0=22,
                       chip_set1=23, reset=24)

BUTTON_ONE = 13
BUTTON_TWO = 27
BUTTON_THREE = 17


class MENUS(Enum):
    MAIN = 0
    WEAPON = 1
    LOGS = 2


class Menus:
    cursor = 0
    state = MENUS.MAIN

    @staticmethod
    def print_menu():
        global GLCD
        GLCD.set_cursor(0, 0, 0)
        GLCD.print_str("Please choose a menu:\n\n")
        GLCD.print_str("# Show weapon list\n", Menus.cursor == 0)
        GLCD.print_str("# Show all logs", Menus.cursor == 1)

    @staticmethod
    def weapon_list(weapon_list):
        print("shouldn't be here yet")
        # pass

    @staticmethod
    def all_logs(log_list):
        global GLCD
        GLCD.set_cursor(0, 0, 0)
        GLCD.print_str('name room in  Time\n')
        start = Menus.cursor - 5 if Menus.cursor - 5 > 0 else 0
        for idx, w in enumerate(log_list[start:start + 6]):
            GLCD.print_str(f'{w[0]: <6} {w[1]: <5} {w[2]: <3} {w[3]}\n',
                           idx == Menus.cursor if Menus.cursor <= 5 else idx == 5)
            if idx == 5:  # ran out of space
                GLCD.set_cursor(0, 7, 60)
                if start != (len(log_list) - 6):
                    GLCD.print_chr(chr(0x7F))  # print down arrow
                else:
                    GLCD.print_str('  ')
                break

    FUNC_LIST = [weapon_list.__func__, all_logs.__func__]


def up_press(channel):
    print("UP PRESSED")
    if Menus.state == MENUS.MAIN:
        if Menus.cursor > 0:
            Menus.cursor -= 1
        Menus.print_menu()
    elif Menus.state == MENUS.WEAPON:
        pass
    elif Menus.state == MENUS.LOGS:
        if Menus.cursor > 0:
            Menus.cursor -= 1
        Menus.all_logs(ll)


def down_press(channel):
    print('DOWN PRESSED')
    if Menus.state == MENUS.MAIN:
        if Menus.cursor < 1:
            Menus.cursor += 1
        Menus.print_menu()
    elif Menus.state == MENUS.WEAPON:
        pass
    elif Menus.state == MENUS.LOGS:
        if Menus.cursor < len(ll) - 1:
            Menus.cursor += 1
        Menus.all_logs(ll)


def select_press(channel):
    global GLCD
    if Menus.state == MENUS.MAIN:
        GLCD.clear()
        Menus.state = MENUS(Menus.cursor + 1)
        Menus.cursor = 0
        Menus.FUNC_LIST[Menus.state.value - 1](ll)


GPIO.setup(BUTTON_ONE, GPIO.IN)
GPIO.setup(BUTTON_TWO, GPIO.IN)
GPIO.setup(BUTTON_THREE, GPIO.IN)

GPIO.add_event_detect(BUTTON_ONE, GPIO.RISING, callback=up_press, bouncetime=500)
GPIO.add_event_detect(BUTTON_TWO, GPIO.RISING, callback=down_press, bouncetime=500)
GPIO.add_event_detect(BUTTON_THREE, GPIO.RISING, callback=select_press, bouncetime=500)


def main():
    global GLCD
    GLCD.start()
    Menus.print_menu()
    input()
    GLCD.clear()


if __name__ == "__main__":
    main()
