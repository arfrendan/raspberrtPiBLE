from escpos.printer import Usb
import six
import sys
#import argparse
'''
parser = argparse.ArgumentParser()
parser.add_argument('--size',help = 'the size of the text',type = int)
parser.add_argument('--command',help = "the command to the printer 'set' 'text' 'cut'",type = str,required = True )
parser.add_argument('--underline',help = 'the underline of the text, default = 0 range 0-2',type = int)
parser.add_argument('--text',help = 'the text you want to print',type = str)
parser.add_argument('--align',help = 'text align, 0 = left, 1 = center ,2 = right',type = int)
parser.add_argument('--texttype',help = 'text type B,U,U2,BU,BU2,NORMAL,',type = str,choices = ['B','U','BU','U2','BU2','NORMAL'])

args = parser.parse_args()
'''

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
        #self.set(width = 1,height = 1)
        if txt:
            self.text(txt)
            self.text("\n")
    
p2 = ChUsb(0x8866,0x0100,timeout=0, in_ep=0x81, out_ep=0x02)

lines = sys.argv[1].split(';;')
if(p2):
    p2.reset()
    for i in lines:
        commands  = i.split(' ')
        command = commands[0]
        
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



'''
if(args.command == 'set'):
    if(args.size):
        p2.set(width = args.size,height = args.size)
        
    if(args.underline):
        p2.set(underline = args.underline)
        
    if(args.align ==0):
        p2.set(align = u'left')
    elif(args.align == 1):
        p2.set(align = u'center')
    elif(args.align == 2):
        p2.set(align = u'right')
        
    if(args.texttype):
        p2.set(text_type=args.texttype)
if(args.command == 'text'):
    if(args.text):
        p2.textln(args.text)
    else:
        print('no content')
if(args.command == 'cut'):
    p2.cut()
if(args.command == 'set'):
    p2.reset()
'''
'''
p2.set(width = 3,height = 3)
p2.textln('黑')
p2.set()
p2.text('黑')
'''
