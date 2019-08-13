from escpos.printer import Usb
import six
import sys
import escpos
align = 'left'
size = 1
texttype = 'normal'
newalign = 'left'
newsize = '1'
newtexttype = 'normal'
class ChUsb (Usb):
    def __init__(self, *args, **kwargs):
        super(ChUsb,self).__init__(*args,**kwargs)
        self.charcode('WPC1252')
    def text(self,txt):
        txt = txt.encode('gb2312').decode('l1')
        if txt:
            if self.codepage:
                self._raw(txt.encode(self.codepage))
            else:
                self._raw(txt.encode())
                
    def reset(self):
        self.set(align = u'left',width = 1,height = 1,text_type = 'NORMAL' )
    def textln(self,txt):
        if txt:
            self.text(txt)
            self.text("\n")

def print_text(text):
    try:
        p2 = ChUsb(0x8866,0x0100,timeout=0, in_ep=0x81, out_ep=0x02)
    except:
        print("no device founded")
        return -1
    lines = text.split(';;')
    if(p2):
        p2.reset()
        for i in lines:
            commands  = i.split(' ')
            command = commands[0]
            print(command)
            if(command == 'text'):
                for j in range(1,len(commands)):
                    p2.text(commands[j]+" ")
                p2.text("\n")
            if(command == 'cut'):
                p2.cut()
            if(command == 'reset'):
                p2.reset()
            if(command == 'set'):
                align = commands[1]
                size = int(commands[2])
                texttype = commands[3]
                p2.set(width = size,height = size,align = align,text_type = texttype)
            if(command == 'line'):
                p2.set(width = 2,height = 2,align = 'left',text_type = 'normal')
                p2.text('------------------------')
                p2.set(width = size,height = size,align = align,text_type = texttype)
    
        