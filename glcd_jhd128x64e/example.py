import jhd_glcd  # glcd_jhd128x64e
import time
import numpy as np
      
def main():
    GLCD = jhd_glcd.KS0108(rs=4, rw=7, en=8, d0=9, d1=10, 
                              d2=11, d3=14, d4=15, d5=17, 
                              d6=18, d7=25, chip_set0=22, 
                              chip_set1=23, reset=24)
    GLCD.start()
    GLCD.set_cursor(0,0,0)
    # GLCD.data_write(0b00000001, 1)
    print(GLCD.Line_Num, GLCD.Cursor_Pos)
    GLCD.draw_line(0,5,128,5)
    print(GLCD.mat[5])
    #GLCD.draw_line(45, 0, 45, 63)
    #GLCD.set_cursor(0,0,50)
    #GLCD.print_str("Logs")
    #GLCD.draw_line(76,0,76,63)
        
            
if __name__ == "__main__":
    main()
