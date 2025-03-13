#!/usr/bin/env python3
import struct
# -*- coding: utf-8 -*-


'''
0000000000111110000000000000000000000000001111100000000000111110
0000000001111111000000000000000000000000011111110000000001111111
1000000011111111000000000000000010000000111111111000000011111111
1000000011000001000000000000000010000000110000011000000011000001

'''

def visualizeData(data_list, str="Data"):
    print(str)
    W,H = struct.unpack_from("<HH", data_list[0].to_bytes(4, byteorder='little', signed=False))
    print(f"{W}x{H}")
    line=0
    for val in data_list[1:]:
        # Handle negative or large values properly by masking to 32 bits
        unsigned_val = val & 0xFFFFFFFF
        bin_str_b0 = format((unsigned_val>>(8*0))&0xff, '08b')  # 32-bit binary with leading zeros
        bin_str_b1 = format((unsigned_val>>(8*1))&0xff, '08b')
        bin_str_b2 = format((unsigned_val>>(8*2))&0xff, '08b')
        bin_str_b3 = format((unsigned_val>>(8*3))&0xff, '08b')
        #print(f"{bin_str_b0}{bin_str_b1}{bin_str_b2}{bin_str_b3}",end="")
        print(f"{unsigned_val:032b}", end="")
        line=line+1
        if(W<=8):
          print("")
        else:
          if(0==line%2):
            print("")
          
    print("|       |       |       |")
    print("01234567012345670123456701234567")

def main():
    # EGA DATA array
    '''
  'BananaLeft

  DATA 458758,202116096,471604224,943208448,943208448,943208448,471604224,202116096,0

  'BananaDown

  DATA 262153, -2134835200, -2134802239, -2130771968, -2130738945,8323072, 8323199, 4063232, 4063294

  'BananaUp

  DATA 262153, 4063232, 4063294, 8323072, 8323199, -2130771968, -2130738945, -2134835200,-2134802239

  'BananaRight

  DATA 458758, -1061109760, -522133504, 1886416896, 1886416896, 1886416896,-522133504,-1061109760,0
    '''
    data_left = [458758,202116096,471604224,943208448,943208448,943208448,471604224,202116096,0]
    data_down = [262153, -2134835200, -2134802239, -2130771968, -2130738945,8323072, 8323199, 4063232, 4063294]
    data_up = [262153, 4063232, 4063294, 8323072, 8323199, -2130771968, -2130738945, -2134835200,-2134802239]
    data_right = [458758, -1061109760, -522133504, 1886416896, 1886416896, 1886416896,-522133504,-1061109760,0]
    
    # Convert each integer to 32-bit binary string
    visualizeData(data_left, "Banana Left")
    visualizeData(data_down, "Banana Down")
    visualizeData(data_up, "Banana Up")
    visualizeData(data_right, "Banana Right")

if __name__ == '__main__':
    main()
