import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from p_exercise_program import Ui_MainWindow
from p_login import LoginWindow
from p_help import Ui_Help
from p_profile import Ui_Profile
from p_ilerlemeraporu import ProgressReport
import subprocess

class Ui_main_menu(object):
    def __init__(self):
        self.main_menu = None
        self.exercise_window = None
        self.help_window = None
        self.profile_window = None
        self.progress_report_window = None
        self.calibration_window = None
        self.opened_windows = []  # Açılan pencereleri saklayacak liste

    def open_exercise_program(self):
        if not self.exercise_window:  # Pencere oluşturulmamışsa oluştur
            self.exercise_window = QtWidgets.QMainWindow()
            self.ui = Ui_MainWindow()
            self.ui.setupUi(self.exercise_window)
            self.opened_windows.append(self.exercise_window)

        self.exercise_window.show()
        self.exercise_window.raise_()

    def open_calibration(self):
        self.calibration_window = subprocess.Popen([sys.executable, "main.py"])
         

    def back_to_login(self):
        self.window = LoginWindow()
        self.window.show()
        self.opened_windows.append(self.window)  # Pencereyi listeye ekle
        self.close_all_windows()

    def open_help_page(self):
        if not self.help_window:
           self.help_window = QtWidgets.QMainWindow()
           self.ui_help = Ui_Help()
           self.ui_help.setupUi(self.help_window)
           self.opened_windows.append(self.help_window)
        self.help_window.show()
        self.help_window.raise_()

    def open_profile_page(self):
      if not self.profile_window:
        self.profile_window = QtWidgets.QMainWindow()
        self.ui_profile = Ui_Profile()
        self.ui_profile.setupUi(self.profile_window)
        self.opened_windows.append(self.profile_window)
      self.profile_window.show()
      self.profile_window.raise_()

    def open_progress_report(self):
      if not self.progress_report_window:
        self.progress_report_window = ProgressReport()
        self.opened_windows.append(self.progress_report_window)

      self.progress_report_window.show()
      self.progress_report_window.raise_()

    def close_all_windows(self):
        for window in self.opened_windows:
            window.close()  # Tüm pencereleri kapat
        self.opened_windows = []# Pencere listesini temizle
        #self.main_menu.close()  # Ana menüyü de kapat

    def setupUi(self, main_menu):
        self.main_menu = main_menu
        main_menu.setObjectName("main_menu")
        main_menu.resize(1440, 760)

        self.label_photo = QtWidgets.QLabel(main_menu)
        self.label_photo.setGeometry(QtCore.QRect(-40, 0, 1471, 951))
        self.label_photo.setPixmap(QtGui.QPixmap("resimler\\start_menu\\startmenu.jpg"))
        self.label_photo.setScaledContents(True)

        self.b_exercise_program = QtWidgets.QPushButton(main_menu)
        self.b_exercise_program.setGeometry(QtCore.QRect(620, 280, 171, 61))
        self.b_exercise_program.setObjectName("b_exercise_program")
        self.b_exercise_program.setStyleSheet("QPushButton { font-size: 14px; }")  # yazı boyutunu ayarla

        self.b_progress_report = QtWidgets.QPushButton(main_menu)
        self.b_progress_report.setGeometry(QtCore.QRect(620, 380, 171, 61))
        self.b_progress_report.setObjectName("b_progress_report")
        self.b_progress_report.setStyleSheet("QPushButton { font-size: 14px; }")  # yazı boyutunu ayarla


        self.b_calibration = QtWidgets.QPushButton(main_menu)
        self.b_calibration.setGeometry(QtCore.QRect(620, 180, 171, 61))
        self.b_calibration.setObjectName("b_calibration")
        self.b_calibration.setStyleSheet("QPushButton { font-size: 14px; }")  # yazı boyutunu ayarla


        self.b_help = QtWidgets.QPushButton(main_menu)
        self.b_help.setGeometry(QtCore.QRect(620, 480, 171, 61))
        self.b_help.setObjectName("b_help")
        self.b_help.setStyleSheet("QPushButton { font-size: 14px; }")  # yazı boyutunu ayarla

        self.b_profile = QtWidgets.QPushButton(main_menu)
        self.b_profile.setGeometry(QtCore.QRect(620, 80, 171, 61))
        self.b_profile.setObjectName("b_profile")
        self.b_profile.setStyleSheet("QPushButton { font-size: 14px; }")  # yazı boyutunu ayarla


        self.b_close = QtWidgets.QPushButton(main_menu)
        self.b_close.setGeometry(QtCore.QRect(20,20,100,40))
        self.b_close.setObjectName("b_close")
        self.b_close.setStyleSheet("QPushButton { font-size: 14px; }")  # yazı boyutunu ayarla


        self.b_exit = QtWidgets.QPushButton(main_menu)
        self.b_exit.setGeometry(QtCore.QRect(620, 580, 171, 61))
        self.b_exit.setObjectName("b_exit")
        self.b_exit.setStyleSheet("QPushButton { font-size: 14px; }")  # yazı boyutunu ayarla



        # Buton tıklama bağlantıları
        self.b_exercise_program.clicked.connect(self.open_exercise_program)
        self.b_calibration.clicked.connect(self.open_calibration)
        self.b_exit.clicked.connect(self.back_to_login)
        self.b_help.clicked.connect(self.open_help_page)
        self.b_profile.clicked.connect(self.open_profile_page)
        self.b_progress_report.clicked.connect(self.open_progress_report)
        self.b_close.clicked.connect(self.close_all_windows)

        self.retranslateUi(main_menu)
        QtCore.QMetaObject.connectSlotsByName(main_menu)

       # main_menu.showFullScreen() # bu satırı kaldırdık yerine aşağıdaki satır eklendi
        main_menu.show()
    def retranslateUi(self, main_menu):
        _translate = QtCore.QCoreApplication.translate
        main_menu.setWindowTitle(_translate("main_menu", "Ana Menü"))
        self.b_exercise_program.setText(_translate("main_menu", "Egzersiz Programı"))
        self.b_progress_report.setText(_translate("main_menu", "İlerleme Raporu"))
        self.b_calibration.setText(_translate("main_menu", "Hareket Et"))
        self.b_help.setText(_translate("main_menu", "Yardım"))
        self.b_close.setText(_translate("main_menu", "Kapat"))
        self.b_profile.setText(_translate("main_menu", "Profil"))
        self.b_exit.setText(_translate("main_menu", "Çıkış"))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_menu = QtWidgets.QMainWindow()
    ui = Ui_main_menu()
    ui.setupUi(main_menu)
    main_menu.show()
    sys.exit(app.exec_())