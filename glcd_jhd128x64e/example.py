import jhd_glcd  # glcd_jhd128x64e
import time
import numpy as np


def print_menu(GLCD):
    GLCD.set_cursor(0,0,0)
    GLCD.print_str("Please choose a menu:\n\n")
    GLCD.print_str("# Show weapon list\n", True)
    GLCD.print_str("# Show all logs")


def main():
    GLCD = jhd_glcd.KS0108(rs=4, rw=21, en=7, d0=12, d1=16, 
                              d2=26, d3=14, d4=15, d5=17, 
                              d6=18, d7=25, chip_set0=22, 
                              chip_set1=23, reset=24)
    GLCD.start()
    print_menu(GLCD)
        
            
if __name__ == "__main__":
    main()
