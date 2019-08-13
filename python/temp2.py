from escpos.printer import Usb
import escpos
import evdev
import temperature
'''
devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
for device in devices:
    print(device.path,device.name,device.phys)
'''
barcodeScannerName = "HID 0581:020c Keyboard"


def printer_state():
    try:
        p = Usb(0x8866,0x0100,timeout=0, in_ep=0x81, out_ep=0x02)
        return 0
    except escpos.exceptions.USBNotFoundError:
        print("printer not found")
        return -1
        
def scanner_state():
    devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
    for dev in devices:
        if dev.name == barcodeScannerName:
            device = evdev.InputDevice(dev.fn)
            return 0
    return -1
    
if __name__ == '__main__':
    print(printer_state())
    print(scanner_state())
    print(temperature.get_temperature())