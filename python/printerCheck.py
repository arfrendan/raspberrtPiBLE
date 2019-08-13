from escpos.printer import Usb
import sys
import escpos
try:
    p = Usb(0x8866,0x0100,timeout=0, in_ep=0x81, out_ep=0x02)
    print(0,end ='')
except escpos.exceptions.USBNotFoundError:
    print(-1,end='')
