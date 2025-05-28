# Raspberry Pi Pico W ile RFID Tabanlı Devamsızlık Takip Sistemi

## 🎯 Proje Hakkında

Bu proje, **Raspberry Pi Pico** ve **RC522 RFID modülü** kullanarak pratik ve güvenli bir devamsızlık takip sistemi geliştirmeyi amaçlamaktadır. Özellikle sınıf, laboratuvar, küçük ofis gibi ortamlarda kimlik doğrulama ve yoklama süreçlerini otomatikleştirmek için tasarlanmıştır.

## 🚀 Özellikler

- **RFID Kart ile Tanıma:** Her kullanıcıya özel RFID etiketleriyle kolay ve hızlı giriş.
- **Anlık Devamsızlık Kaydı:** Okutulan kartlar anında kayıt altına alınır.
- **RGB LED ile Durum Bildirimi:** Başarılı veya hatalı okuma durumları için renkli görsel uyarılar.
- **Kablosuz Bağlantı (Opsiyonel):** Pico W ile WiFi üzerinden veritabanına kayıt imkânı.
- **Kolay Genişletme:** Sınıfa, ofise veya etkinliğe göre kullanıcı listesi kolayca güncellenebilir.

## 🛠️ Kullanılan Donanımlar

- **Raspberry Pi Pico / Pico W**
- **RC522 RFID Kit**
- **RGB LED Modülü**
- Breadboard, jumper kablolar, RFID kart/anahtarlık

## 🔌 Devre Şeması
 
> <img width="944" alt="devre_şeması" src="https://github.com/user-attachments/assets/8000f212-06ce-4db7-9c74-3714b05bc7f6" />


## 💻 Yazılım Hakkında

Projede MicroPython dili kullanılmıştır. Kart okunduğunda UID bilgisi alınır, tanımlı kullanıcılar kontrol edilir ve kayıt işlemi yapılır. İsteğe bağlı olarak, bu kayıtlar WiFi üzerinden merkezi bir veritabanına gönderilebilir.

### Temel Kod Akışı:
1. RFID kart okutulur

```python
from mfrc522 import MFRC522
import utime
 
reader = MFRC522(spi_id=0,sck=6,miso=4,mosi=7,cs=5,rst=22)
 
print("RFID kartını yaklaştırın...")
print("")
```

3. Kart UID’si kontrol edilir

```python
while True:
    reader.init()
    (stat, tag_type) = reader.request(reader.REQIDL)
    if stat == reader.OK:
        (stat, uid) = reader.SelectTagSN()
        if stat == reader.OK:
            card = int.from_bytes(bytes(uid),"little",False)
            print("CARD ID: "+str(card))
utime.sleep_ms(500) 
```

4. Kayıt alınır ve RGB LED ile kullanıcıya bilgi verilir:

- Başarılı okuma durumunda devamsızlık kaydı alınır, RGB LED yeşil yanar.

```python
if card == 822265293:
     print("Card ID: "+ str(card)+" ONAY: Yeşil Işık Yakıldı")
     red.value(0)
     green.value(1)
     blue.value(0)
```

- Tanımsız kartta veya hata durumunda kırmızı ışık yanar.

```python
 else:
     print("Card ID: "+ str(card)+" BİLİNMEYEN KART! Kırmızı Işık Yakıldı")
     red.value(1)
     green.value(0)
     blue.value(0)
```

5. Kayıtlar internet üzerinden veritabanına aktarılır

```python
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
```

## ☁️ Veritabanı Entegrasyonu

Firebase ile bulut tabanlı bir veritabanı sistemi entegre edilebilir. Raspberry Pi Pico W modeli WI-FI desteği sayesinde kartı okur ve gelen ID’yi Firebase’e iletir.

### *Firebase Ayarları

-Firebase Console’dan yeni bir proje açın.

-Realtime Database veya Firestore’u başlatın.

-Kurallar kısmında test için şunu kullanabilirsiniz (güvenlik için sadece testte!):

``` JSON
{
  "rules": {
    ".read": true,
    ".write": true
  }
}
```

## 🧑‍💻 Kurulum ve Kullanım

1. Donanımı bağlantı şemasına göre kurun.
2. Kodları Raspberry Pi Pico’ya yükleyin.
3. Sistemi başlatın ve kart okutun!


