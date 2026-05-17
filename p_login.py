
import sys
from PyQt5 import QtWidgets, QtGui, QtCore
import os
import subprocess

class LoginWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Pencere özellikleri
        self.setWindowTitle("Giriş Ekranı")
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)  # Pencere kapatıldığında belleği temizle

        # Arka Plan
        self.background_label = QtWidgets.QLabel(self)
        self.background_pixmap = QtGui.QPixmap(os.path.expanduser("resimler\\login.jpeg"))
        self.background_label.setPixmap(self.background_pixmap)
        self.background_label.setScaledContents(True)  # Resmi ölçeklendir
        self.background_label.setGeometry(0, 0, self.width(), self.height())  # Tam ekran boyutları

        # Başlık Barı
        self.title_bar = QtWidgets.QWidget(self)
        self.title_bar.setStyleSheet("background: rgba(44, 62, 80, 0.8); border-top-left-radius: 15px; border-top-right-radius: 15px;")  # Şeffaf arka plan
        self.title_bar.setFixedHeight(40)  # Başlık barı yüksekliği
        self.title_bar.setObjectName("title_bar")

        # Minimize Butonu
        self.minimize_button = QtWidgets.QPushButton("_", self.title_bar)
        self.minimize_button.setStyleSheet("background: #34495e; color: #ecf0f1; border: none; font-size: 18px;")
        self.minimize_button.clicked.connect(self.show)

        # Close Butonu
        self.close_button = QtWidgets.QPushButton("X", self.title_bar)
        self.close_button.setStyleSheet("background: #e74c3c; color: #ecf0f1; border: none; font-size: 18px;")
        self.close_button.clicked.connect(self.close)

        # İçerik Container
        self.content_container = QtWidgets.QWidget(self)
        self.content_container.setStyleSheet("background: rgba(255, 255, 255, 0.5); border-radius: 44px;")  # Şeffaf arka plan

        # Hoşgeldiniz Başlığı Çerçevesi
        self.title_background = QtWidgets.QWidget(self.content_container)
        self.title_background.setStyleSheet("background: rgba(255, 255, 255, 0.1); border-radius: 40px; color:6A5ACD;")  # Şeffaf arka plan

        # Hoşgeldiniz Başlığı
        self.title_label = QtWidgets.QLabel("Hoşgeldiniz!", self.title_background)
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 40px; font-weight: bold; color: #21374A;")

        # Kullanıcı Adı Barı
        self.username_input = QtWidgets.QLineEdit(self.content_container)
        self.username_input.setStyleSheet(self.input_style())
        self.username_input.setPlaceholderText("Kullanıcı Adınızı Girin")

        # Parola Barı
        self.password_input = QtWidgets.QLineEdit(self.content_container)
        self.password_input.setStyleSheet(self.input_style())
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_input.setPlaceholderText("Parolanızı Girin")

        # Beni Hatırla Checkbox
        self.remember_me_checkbox = QtWidgets.QCheckBox("Beni Hatırla", self.content_container)
        self.remember_me_checkbox.setStyleSheet("font-size: 14px; color: #2c3e50;")

        # Giriş Butonu
        self.login_button = QtWidgets.QPushButton("Giriş", self.content_container)
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #ffffff; 
                color: #000000; 
                font-size: 18px; 
                padding: 10px; 
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.login_button.clicked.connect(self.check_login)

        # Başarı Mesajı ve İkonu
        self.success_message_label = QtWidgets.QLabel(self.content_container)
        self.success_message_label.setAlignment(QtCore.Qt.AlignCenter)
        self.success_message_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #2ecc71;")  # Yeşil renk ve kalın yazı
        self.success_message_label.setVisible(False)  # Başlangıçta görünmez

        self.is_dragging = False
        self.drag_start_position = None
        self.title_bar.mousePressEvent = self.mouse_press_event
        self.title_bar.mouseMoveEvent = self.mouse_move_event

        self.setup_ui()

    def setup_ui(self):
        # Pencere boyutları ayarlandı
        screen_geometry = QtWidgets.QApplication.desktop().screenGeometry()
        self.setGeometry(screen_geometry)  # Tam ekran

        # Arka plan resmi ayarlandı
        self.background_label.setGeometry(0, 0, screen_geometry.width(), screen_geometry.height())

        # Başlık barı konumlandırıldı
        self.title_bar.setGeometry(0, 0, self.width(), 40)  # Başlık barı koordinatları
        self.title_bar.setFixedWidth(self.width())  # Genişlik ayarlandı

        # İçerik konteyneri ayarlandı
        self.content_container.setGeometry(50, 60, self.width() - 100, self.height() - 100)  # İçerik container koordinatları

        # Hoşgeldiniz başlığı ayarlandı
        self.title_background.setGeometry(0, 0, self.content_container.width(), 80)  # Başlık arka planının koordinatları
        self.title_label.setGeometry(0, 0, self.content_container.width(), 80)  # Başlık koordinatları

        # Kullanıcı adı ve parola barları ayarlandı (ölçüleri artırıldı)
        self.username_input.setGeometry(175, 100, 350, 60)  # Kullanıcı adı barı koordinatları ve boyut
        self.password_input.setGeometry(175, 180, 350, 60)  # Parola barı koordinatları ve boyut

        # Checkbox ve Giriş butonu ayarlandı (ölçüleri artırıldı)
        self.remember_me_checkbox.setGeometry(175, 270, 200, 30)  # Checkbox koordinatları ve boyut
        self.login_button.setGeometry(250, 330, 150, 50)  # Giriş butonu koordinatları ve boyut

        # Başarı mesajı ve ikonu ayarlandı
        self.success_message_label.setGeometry(175, 320, 250, 40)  # Mesaj koordinatları

        # Butonların konumları ve boyutları dinamik olarak ayarlandı
        self.minimize_button.setGeometry(self.width() - 60, 5, 30, 30)  # Minimize butonu koordinatları
        self.close_button.setGeometry(self.width() - 30, 5, 30, 30)  # Close butonu koordinatları

    def input_style(self):
        return """
            QLineEdit {
                padding: 10px;
                border: 2px solid #3498db;
                border-radius: 10px;
                background-color: #f7f9f9;
                color: #2c3e50;
                font-size: 16px;
            }
            QLineEdit:focus {
                border-color: #2980b9;
            }
        """

    def mouse_press_event(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.is_dragging = True
            self.drag_start_position = event.globalPos() - self.frameGeometry().topLeft()

    def mouse_move_event(self, event):
        if self.is_dragging:
            self.move(event.globalPos() - self.drag_start_position)

    def check_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if username == "hasan" and password == "12345":
            self.show_success_message()  # Giriş başarılı olduğunda mesaj göster
            # Check if "Beni Hatırla" is checked and save the login state
            if self.remember_me_checkbox.isChecked():
                with open("login_state.txt", "w") as file:
                    file.write(f"{username}\n{password}")
            QtCore.QTimer.singleShot(2000, self.open_main_menu)  # Wait 2 seconds before opening the main menu
        else:
            self.show_error_message("Kullanıcı adı veya şifre yanlış!")

    def show_error_message(self, message):
        error_dialog = QtWidgets.QMessageBox()
        error_dialog.setWindowTitle("Hata")
        error_dialog.setText(message)
        error_dialog.setIcon(QtWidgets.QMessageBox.Warning)
        error_dialog.setStyleSheet("QMessageBox { background-color: #ffffff; }")
        error_dialog.setGeometry(self.geometry().center().x() - 150, self.geometry().center().y() - 50, 300, 100)
        error_dialog.exec_()

    def show_success_message(self):
        self.success_message_label.setText("Lütfen Bekleyiniz")
        self.success_message_label.setVisible(True)
        screen_geometry = QtWidgets.QApplication.desktop().screenGeometry()
        message_geometry = self.success_message_label.geometry()
        x = (screen_geometry.width() - message_geometry.width()) / 2
        y = (screen_geometry.height() - message_geometry.height()) / 2
        self.success_message_label.move(int(x), int(y))

    def open_main_menu(self):
        try:
            subprocess.Popen([sys.executable, "start_menu.py"])
            self.close()
        except FileNotFoundError:
            error_dialog = QtWidgets.QMessageBox()
            error_dialog.setWindowTitle("Hata")
            error_dialog.setText("main_menu.py dosyası bulunamadı!")
            error_dialog.setIcon(QtWidgets.QMessageBox.Critical)
            error_dialog.exec_()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    login_window = LoginWindow()

    # Check if there is a saved login state
    if os.path.exists("login_state.txt"):
        with open("login_state.txt", "r") as file:
            saved_username = file.readline().strip()
            saved_password = file.readline().strip()
            login_window.username_input.setText(saved_username)
            login_window.password_input.setText(saved_password)
            login_window.remember_me_checkbox.setChecked(True)

    login_window.show()  # Normal modda göster
    sys.exit(app.exec_())
