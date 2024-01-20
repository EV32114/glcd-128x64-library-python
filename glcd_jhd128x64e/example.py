import jhd_glcd  # glcd_jhd128x64e
import time
import numpy as np


def list_weapons(GLCD, l):
    GLCD.clear()
    GLCD.set_cursor(0,0,0)
    GLCD.print_str('name room in  Time\n')
    chosen = 0
    start = 0
    user_input = ''
    while user_input != 'exit':
        GLCD.set_cursor(0,1,0)
        for idx, w in enumerate(l[start:start+6]):
            GLCD.print_str(f'{w[0]: <6} {w[1]: <5} {w[2]: <3} {w[3]}\n', idx==chosen if chosen <= 5 else idx==5)
            if idx==5:  # ran out of space
                GLCD.set_cursor(0,7,60)
                if start != (len(l) - 6):
                    GLCD.print_chr(chr(0x7F))  # print down arrow
                else:
                    GLCD.print_str('  ')
                break
        user_input = input()
        if user_input != 'exit':
            if user_input == 'u' and chosen < len(l) - 1:
                chosen += 1
                if chosen > 5:
                    start += 1
            elif user_input == 'd' and chosen > 0:
                chosen -= 1
                if chosen >= 5:
                    start -= 1


def print_menu(GLCD):
    l = []
    for i in range(10):
        l.append([f'w{i}', f'lab{(i % 2) + 1}', i % 2, '12.1  11:25'])
    x=''
    while x=='':
        GLCD.set_cursor(0,0,0)
        GLCD.print_str("Please choose a menu:\n\n")
        GLCD.print_str("# Show weapon list\n", True)
        GLCD.print_str("# Show all logs")
        x=input()
        if x!='':
            break
        GLCD.set_cursor(0,2,0)
        GLCD.print_str("# Show weapon list\n")
        GLCD.print_str("# Show all logs", True)
        x=input()
        if x != '':
            list_weapons(GLCD, l)
            break


def main():
    GLCD = jhd_glcd.KS0108(rs=4, rw=21, en=7, d0=12, d1=16, 
                              d2=26, d3=14, d4=15, d5=17, 
                              d6=18, d7=25, chip_set0=22, 
                              chip_set1=23, reset=24)
    GLCD.start()
    print_menu(GLCD)
    GLCD.clear()


if __name__ == "__main__":
    main()
