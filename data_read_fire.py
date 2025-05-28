from mfrc522 import MFRC522
import utime

try:
    import urequests as requests  # MicroPython için
except:
    import requests  # Normal Python için (test amaçlı)

import network

# Wi-Fi ayarları (Pico W veya ESP32 için)
SSID = "[WIFI ADI]"
PASSWORD = "[WIFI SIFRESI]"

# Firebase ayarları
FIREBASE_URL = "https://[Proje_İsmi].firebaseio.com/devamsizlik.json"

def wifi_baglan():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Wi-Fi'ye bağlanılıyor...")
        wlan.connect(SSID, PASSWORD)
        while not wlan.isconnected():
            utime.sleep(1)
    print("Bağlandı:", wlan.ifconfig())

wifi_baglan()

reader = MFRC522(spi_id=0, sck=6, miso=4, mosi=7, cs=5, rst=22)

print("RFID kartını yaklaştırın...\n")

while True:
    reader.init()
    (stat, tag_type) = reader.request(reader.REQIDL)
    if stat == reader.OK:
        (stat, uid) = reader.SelectTagSN()
        if stat == reader.OK:
            card = int.from_bytes(bytes(uid),"little",False)
            print("CARD ID: "+str(card))
            
            # Firebase'e gönderilecek veri
            data = {
                "card_id": str(card),
                "timestamp": utime.time()
            }
            try:
                response = requests.post(FIREBASE_URL, json=data)
                print("Firebase yanıtı:", response.text)
                response.close()
            except Exception as e:
                print("Firebase hatası:", e)
    utime.sleep_ms(500)
