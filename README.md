# Real-Time Human Joint Angle Tracking and Control

Bu proje, insan eklem acilarini gercek zamanli olarak takip edip referans egzersiz hareketleriyle karsilastiran bir PyQt5 masaustu uygulamasidir.

## Proje Ozeti
- Kamera akisi uzerinden vucut pozunu algilar (MediaPipe Pose).
- Omuz, dirsek, kalca, diz ve ayak bilegi gibi eklem acilarini hesaplar.
- Referans hareket gorselleri ile canli hareketi tolerans degeri icinde karsilastirir.
- Kullaniciya egzersiz, profil, yardim ve ilerleme raporu ekranlari sunar.

## Kullanilan Teknolojiler
- Python 3
- PyQt5
- OpenCV
- MediaPipe
- NumPy

## Proje Akisi
1. Giris ekrani acilir.
2. Ana menuden profil, kalibrasyon (hareket et), egzersiz programi, yardim ve ilerleme raporu ekranlarina gecilir.
3. Egzersiz ekraninda `hareketler/` klasorundeki referans gorseller sira ile islenir.
4. Kamera akisi ile acisal dogruluk kontrolu yapilir.

## Ekran Goruntuleri

### Giris
![Giris ekrani](Görüntüler/giris/1.8%20log%20in%20ekranı.PNG)

### Ana Menu
![Ana menu](Görüntüler/start_menu/1.1%20start%20menu.PNG)

### Egzersiz
![Egzersiz ekrani](Görüntüler/egzersiz/1.4%20egzersiz%20programı.PNG)

### Yardim
![Yardim ekrani](Görüntüler/yardim/1.7%20yardım.PNG)

### Ilerleme Raporu
![Ilerleme raporu](Görüntüler/ilerleme_raporu/1.6%20ilerleme%20raporu.PNG)

## Kurulum
Asagidaki paketleri yukleyin:

```bash
pip install pyqt5 opencv-python mediapipe numpy
```

## Calistirma
Proje klasorunde terminal acip su komutu calistirin:

```bash
python start_menu.py
```

Alternatif olarak giris ekraniyla baslamak icin:

```bash
python p_login.py
```

## Giris Bilgisi (Demo)
- Kullanici adi: `hasan`
- Sifre: `12345`

## Klasor Yapisi (Ozet)
```text
StajProjesiiii/
  start_menu.py
  main.py
  p_login.py
  p_profile.py
  p_help.py
  p_ilerlemeraporu.py
  p_exercise_program.py
  hareketler/            # Referans egzersiz gorselleri
  resimler/              # Uygulama arka plan ve tema gorselleri
  Görüntüler/            # Dokumantasyon ekran goruntuleri
```

## Notlar
- Kamera erisimi aktif olmalidir.
- Uygulama icinde Python sureci gecisleri `sys.executable` ile calisacak sekilde duzenlenmistir.
- Isletim sistemi olarak Windows ortaminda test edilmistir.
