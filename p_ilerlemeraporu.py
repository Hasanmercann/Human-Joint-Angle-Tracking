
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton,
     QHBoxLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import subprocess

class ProgressReport(QMainWindow):  # Pencere ismini değiştirdik
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Progress Report")  # Pencere başlığını değiştirdik
        #self.setGeometry(100, 100, 1500, 800)
        self.setGeometry(100, 100, 1920, 1080)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Arka plan resmi için QLabel
        self.background_label = QLabel(self)
        self.background_label.setScaledContents(True)
        self.set_background_image("resimler\\rapor.jpg")

        # Ana düzeni ayarla
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(20)

        # Geri Dön butonunu ekle
        self.back_button = QPushButton("Geri Dön", self)
        self.back_button.setStyleSheet(
            "background-color: #E57373; color: white; border-radius: 10px; padding: 8px; font-size: 16px;"
        )
        self.back_button.clicked.connect(self.go_back)  # Geri Dön butonuna tıklama işlemi bağlanıyor

        # Butonları ve açıklama alanlarını ayarlamak için düzenler
        self.left_button_layout = QVBoxLayout()
        self.right_button_layout = QVBoxLayout()
        self.description_layout = QVBoxLayout()

        # Açıklama etiketi
        self.description_label = QLabel(self)
        self.description_label.setWordWrap(True)
        self.description_label.setAlignment(Qt.AlignCenter)
        self.description_label.setStyleSheet(
            "font-size: 18px; color: black; padding: 10px;"
            "background-color: rgba(255, 255, 255, 0.3);"
            "border-radius: 10px;"
        )
        self.description_label.setFixedHeight(200)

        # Açıklama düzenine ekle
        self.description_layout.addWidget(self.description_label)
        self.main_layout.addLayout(self.description_layout)

        # Bölümleri tanımla
        self.sections = {
            "Kullanıcı Bilgileri": self.user_info(),
            "Egzersiz Verileri": self.exercise_data(),
            "İlerlemenin Görselleştirilmesi": self.visualization(),
            "Sağlık Verileri": self.health_data(),
            "Notlar ve Geri Bildirim": self.notes_feedback(),
            "Öneriler ve Hedefler": self.suggestions_goals(),
            "Zaman Çizelgesi": self.timeline(),
            "Açıklayıcı Bilgiler": self.explanatory_info(),
            "Sonuçlar ve Öneriler": self.results_suggestions()
        }

        # Butonları oluştur ve yerleştir
        for i, (title, description) in enumerate(self.sections.items()):
            button = QPushButton(title)
            button.setStyleSheet(self.button_style(i))
            button.setToolTip(description)
            button.clicked.connect(lambda checked, desc=description: self.show_description(desc))

            if i % 2 == 0:
                self.left_button_layout.addWidget(button)
            else:
                self.right_button_layout.addWidget(button)

        # Geri Dön butonunu sol üst köşeye yerleştir
        self.left_button_layout.insertWidget(0, self.back_button)
        self.main_layout.addLayout(self.left_button_layout)
        self.main_layout.addLayout(self.right_button_layout)

        # Başlangıçta Kullanıcı Bilgileri açıklamasını göster
        self.show_description(self.sections["Kullanıcı Bilgileri"])

    def button_style(self, index):
        # Buton stilleri
        if index % 2 == 0:
            return """
            QPushButton {
                background-color: #6CA6E5; 
                color: white;  
                border-radius: 10px;  
                padding: 10px;  
                font-size: 18px;  
                border: none;  
                min-width: 150px;  
                max-width: 300px;  
            }
            QPushButton:hover {
                background-color: #5A9BC1;  
            }
            QPushButton:pressed {
                background-color: #4B8B9D;  
            }
            """
        else:
            return """
            QPushButton {
                background-color: #5A9BC1;  
                color: white;  
                border-radius: 10px;  
                padding: 10px;  
                font-size: 18px;  
                border: none;  
                min-width: 150px;  
                max-width: 300px;  
            }
            QPushButton:hover {
                background-color: #4B8B9D;  
            }
            QPushButton:pressed {
                background-color: #3C7A8D;  
            }
            """

    def set_background_image(self, path):
        pixmap = QPixmap(path)
        self.background_label.setPixmap(pixmap)
        self.background_label.setGeometry(self.rect())
        self.background_label.lower()

    # Bölüm açıklamaları
    def user_info(self):
        return (
            "<b>Ad:</b> Kullanıcının tam adı.<br>"
            "<b>Yaş:</b> Kullanıcının yaşı.<br>"
            "<b>Cinsiyet:</b> Kullanıcının cinsiyeti.<br>"
            "<b>Başlangıç Tarihi:</b> Egzersiz programına başladığı tarih.<br>"
            "<b>Hedef Tarihi:</b> Hedeflenen sona ulaşılması beklenen tarih.<br>"
            "Bu bilgiler, kullanıcının kişisel geçmişi ve hedeflerini anlamak için önemlidir."
        )

    def exercise_data(self):
        return (
            "<b>Egzersiz Türü:</b> Yapılan egzersizlerin türleri (örneğin, esneme, güçlendirme, kardiyo).<br>"
            "<b>Egzersiz Süresi:</b> Her egzersiz seansı için harcanan süre (dakika cinsinden).<br>"
            "<b>Tekrar Sayısı:</b> Yapılan tekrar sayıları (örneğin, 3 set x 10 tekrar).<br>"
            "Bu veriler, kullanıcının performansını değerlendirmek için kullanılır."
        )

    def visualization(self):
        return (
            "<b>Grafikler:</b> Egzersiz süreleri, tekrar sayıları ve kilo gibi verilerin zamanla nasıl değiştiğini gösteren grafikler.<br>"
            "<b>İlerleme Çizelgesi:</b> Günlük veya haftalık egzersiz raporları.<br>"
            "Bu grafikler, kullanıcıların gelişimini görsel olarak takip etmelerini sağlar."
        )

    def health_data(self):
        return (
            "<b>Kilo:</b> Kullanıcının başlangıç ve güncel kiloları.<br>"
            "<b>Beden Kitle İndeksi (BKİ):</b> Kullanıcının BKİ değeri.<br>"
            "<b>Diğer Sağlık Verileri:</b> Kalp atış hızı, kan basıncı gibi diğer sağlık parametreleri.<br>"
            "Bu bilgiler, kullanıcıların sağlık durumlarını izlemede kritik bir rol oynar."
        )

    def notes_feedback(self):
        return (
            "<b>Kullanıcı Notları:</b> Kullanıcıların program hakkında eklemek istedikleri kişisel notlar.<br>"
            "<b>Hekim veya Eğitmen Geri Bildirimi:</b> Kullanıcının ilerlemesi hakkında uzmanlardan gelen geri bildirimler.<br>"
            "Bu bölüm, kullanıcıların programın etkisini ve önerilerini kaydetmeleri için bir alan sağlar."
        )

    def suggestions_goals(self):
        return (
            "<b>Gelecek Hedefler:</b> Kullanıcının bir sonraki egzersiz seansında ulaşmayı hedeflediği özel hedefler (örneğin, 5 kg vermek).<br>"
            "<b>Egzersiz Önerileri:</b> Kullanıcı için önerilen yeni egzersizler veya değişiklikler.<br>"
            "Bu bilgiler, kullanıcıların hedeflerine ulaşmalarına yardımcı olmak için yönlendirici bir rol oynar."
        )

    def timeline(self):
        return (
            "<b>Egzersiz Programı:</b> Günlük veya haftalık olarak planlanan egzersizlerin listesi.<br>"
            "<b>İlerleme Raporları:</b> Kullanıcının belirli aralıklarla ne kadar ilerleme kaydettiği.<br>"
            "Bu zaman çizelgesi, kullanıcıların programlarının sürekliliğini sağlamada yardımcı olur."
        )

    def explanatory_info(self):
        return (
            "<b>Egzersizlerin Faydaları:</b> Düzenli egzersiz yapmanın sağlık üzerindeki olumlu etkileri.<br>"
            "<b>Dikkat Edilmesi Gerekenler:</b> Egzersiz sırasında sakatlanmalardan kaçınmak için dikkat edilmesi gereken noktalar.<br>"
            "Bu bilgiler, kullanıcıların programı daha iyi anlamalarına ve güvenle ilerlemelerine yardımcı olur."
        )

    def results_suggestions(self):
        return (
            "<b>Genel Sonuçlar:</b> Kullanıcının başlangıçtan bu yana kaydettiği ilerlemeler.<br>"
            "<b>Uzman Önerileri:</b> Kullanıcının gelecekteki hedefleri için uzmanlardan gelen öneriler.<br>"
            "Bu bölüm, kullanıcının nihai değerlendirmesini ve gelecekteki önerilerini içerir."
        )

    # Geri dönüş işlevi
    def go_back(self):      
        subprocess.Popen([sys.executable, "start_menu.py"]) 


    # Açıklama gösterimi işlevi
    def show_description(self, description):
        self.description_label.setText(description)

    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProgressReport()  # Class ismi "ProgressReport" olarak değiştirildi
    window.show()
    window.show()
    sys.exit(app.exec_())
