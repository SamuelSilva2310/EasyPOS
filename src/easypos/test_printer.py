from escpos.printer import Usb

printer = Usb(idVendor=1046, idProduct=20497, encoding="cp860")
encodings = ["OEM860", "OEM850", "cp1252", "latin1"]
for enc in encodings:
    printer = Usb(idVendor=1046, idProduct=20497, encoding=enc)
    printer.text(f"Test encoding: {enc} - Á, é, ç, ã, õ\n")
printer.cut()