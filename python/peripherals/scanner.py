import evdev
barcodeScannerName = "HID 0581:020c Keyboard"
def scanner():
    devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
    for dev in devices:
        if dev.name == barcodeScannerName:
            device = evdev.InputDevice(dev.fn)
            return 0
    return -1

print(scanner(),end='')
