from machine import Pin
from mfrc522 import MFRC522
import utime
       
reader = MFRC522(spi_id=0,sck=6,miso=4,mosi=7,cs=5,rst=22)
 
red = Pin(0, Pin.OUT)
green = Pin(1, Pin.OUT)
blue = Pin(2, Pin.OUT)
 
print("RFID kartını yaklaştırın...")
print("")
 
 
while True:
    reader.init()
    (stat, tag_type) = reader.request(reader.REQIDL)
    if stat == reader.OK:
        (stat, uid) = reader.SelectTagSN()
        if stat == reader.OK:
            card = int.from_bytes(bytes(uid),"little",False)
            
            if card == 822265293:
                print("Card ID: "+ str(card)+" ONAY: Yeşil Işık Yakıldı")
                red.value(1)
                green.value(0)
                blue.value(0)
                
                
            elif card == 2902757525:
                print("Card ID: "+ str(card)+" ONAY: Yeşil Işık Yakıldı")
                red.value(1)
                green.value(0)
                blue.value(0)
                
            else:
                print("Card ID: "+ str(card)+" BİLİNMEYEN KART! Kırmızı Işık Yakıldı")
                red.value(0)
                green.value(1)
                blue.value(0)
