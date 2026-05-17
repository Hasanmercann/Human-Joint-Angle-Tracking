
import sys
import cv2
import numpy as np
import mediapipe as mp
import os
import time
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import (
    QApplication, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget
)

# Mediapipe modüllerini başlatın
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

# Pose modelini başlatın
pose = mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Sabit açı toleransı (derece)
ANGLE_TOLERANCE = 40

def calculate_angle(a, b, c):
    """Üç nokta arasındaki açıyı hesaplar."""
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    
    v1 = a - b
    v2 = c - b
    
    radians = np.arctan2(v2[1], v2[0]) - np.arctan2(v1[1], v1[0])
    angle = np.abs(radians * 180.0 / np.pi)
    
    if angle > 180.0:
        angle = 360 - angle
        
    return angle

def get_pose_angles(landmarks, image_width, image_height):
    """Verilen landmarklardan eklem açılarını hesaplar ve döndürür."""
    angles = {}
    
    # Helper fonksiyon: Landmark koordinatlarını alır
    def get_coordinates(landmark):
        return [landmark.x * image_width, landmark.y * image_height]
    
    # Sağ Dirsek
    right_shoulder = get_coordinates(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value])
    right_elbow = get_coordinates(landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value])
    right_wrist = get_coordinates(landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value])
    angles['right_elbow'] = calculate_angle(right_shoulder, right_elbow, right_wrist)
    
    # Sol Dirsek
    left_shoulder = get_coordinates(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value])
    left_elbow = get_coordinates(landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value])
    left_wrist = get_coordinates(landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value])
    angles['left_elbow'] = calculate_angle(left_shoulder, left_elbow, left_wrist)
    
    # Sağ Diz
    right_hip = get_coordinates(landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value])
    right_knee = get_coordinates(landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value])
    right_ankle = get_coordinates(landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value])
    angles['right_knee'] = calculate_angle(right_hip, right_knee, right_ankle)
    
    # Sol Diz
    left_hip = get_coordinates(landmarks[mp_pose.PoseLandmark.LEFT_HIP.value])
    left_knee = get_coordinates(landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value])
    left_ankle = get_coordinates(landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value])
    angles['left_knee'] = calculate_angle(left_hip, left_knee, left_ankle)
    
    # Sağ Omuz
    angles['right_shoulder'] = calculate_angle(right_hip, right_shoulder, right_elbow)
    
    # Sol Omuz
    angles['left_shoulder'] = calculate_angle(left_hip, left_shoulder, left_elbow)
    
    # Sağ Kalça
    angles['right_hip_angle'] = calculate_angle(right_shoulder, right_hip, right_knee)
    
    # Sol Kalça
    angles['left_hip_angle'] = calculate_angle(left_shoulder, left_hip, left_knee)
    
    # Sağ Bilek
    right_thumb = get_coordinates(landmarks[mp_pose.PoseLandmark.RIGHT_THUMB.value])
    angles['right_wrist'] = calculate_angle(right_elbow, right_wrist, right_thumb)
    
    # Sol Bilek
    left_thumb = get_coordinates(landmarks[mp_pose.PoseLandmark.LEFT_THUMB.value])
    angles['left_wrist'] = calculate_angle(left_elbow, left_wrist, left_thumb)
    
    # Sağ Ayak Bileği
    right_heel = get_coordinates(landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value])
    angles['right_ankle'] = calculate_angle(right_knee, right_ankle, right_heel)
    
    # Sol Ayak Bileği
    left_heel = get_coordinates(landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value])
    angles['left_ankle'] = calculate_angle(left_knee, left_ankle, left_heel)
    
    # Baş
    nose = get_coordinates(landmarks[mp_pose.PoseLandmark.NOSE.value])
    left_eye = get_coordinates(landmarks[mp_pose.PoseLandmark.LEFT_EYE.value])
    right_eye = get_coordinates(landmarks[mp_pose.PoseLandmark.RIGHT_EYE.value])
    angles['head'] = calculate_angle(left_eye, nose, right_eye)
    
    return angles

def compare_angles(reference_angles, live_angles, tolerance=ANGLE_TOLERANCE):
    """
    İki açı setini karşılaştırır.
    
    Args:
        reference_angles (dict): Referans pose açıları.
        live_angles (dict): Canlı pose açıları.
        tolerance (int): Açı toleransı (derece).
    
    Returns:
        bool: Tüm açı farkları tolerans içindeyse True, aksi halde False.
    """
    for key, ref_angle in reference_angles.items():
        live_angle = live_angles.get(key, 0)
        if abs(ref_angle - live_angle) > tolerance:
            return False
    return True

def annotate_image(image, landmarks, image_width, image_height):
    """Resme pose landmark'larını çizer."""
    mp_drawing.draw_landmarks(
        image,
        landmarks,
        mp_pose.POSE_CONNECTIONS,
        mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=4),
        mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2)
    )
    return image

def process_reference_images(input_dir):
    """
    Referans resimleri önceden işler ve pose açılarını saklar.
    
    Args:
        input_dir (str): Giriş resimlerinin bulunduğu klasör.
    
    Returns:
        list: Her bir referans pose için bilgiler.
    """
    # Desteklenen resim formatları
    supported_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff')
    
    # Giriş klasöründeki tüm dosyaları listele ve alfabetik olarak sırala
    all_files = os.listdir(input_dir)
    image_files = [f for f in all_files if f.lower().endswith(supported_extensions)]
    image_files.sort()  # Alfabetik sıralama
    
    if not image_files:
        print(f"Giriş klasöründe desteklenen resim bulunamadı: {input_dir}")
        return []
    
    reference_poses = []
    for idx, image_file in enumerate(image_files, start=1):
        image_path = os.path.join(input_dir, image_file)
        print(f"[{idx}/{len(image_files)}] İşleniyor: {image_file}")
        image = cv2.imread(image_path)
        if image is None:
            print(f"Resim yüklenemedi: {image_path}")
            continue
        
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb_image)
        
        if results.pose_landmarks:
            image_height, image_width, _ = image.shape
            angles = get_pose_angles(results.pose_landmarks.landmark, image_width, image_height)
            
            # Referans resmi anotasyon yapmadan sakla
            reference_image = image.copy()
            
            reference_poses.append({
                'annotated_image': reference_image,  # Anotasyon yapmadan sakla
                'angles': angles,
                'name': os.path.splitext(image_file)[0]  # İsimlendirme için dosya adı
            })
            print(f"Poz tespit edildi: {image_file}")
        else:
            print(f"Poz tespit edilemedi: {image_file}")
    
    # Referans pozları rastgele sıraya sokmayı kaldırdık
    # random.shuffle(reference_poses)  # Bu satırı kaldırıyoruz
    # print("Referans pozlar rastgele sıraya sokuldu.")  # Bu satırı kaldırıyoruz
    
    print("Referans pozlar sırasıyla işlendi.")
    return reference_poses

class VideoThread(QThread):
    # Sinyali tanımla: Referans görüntü, canlı görüntü, poz doğru mu, referans poz adı
    change_pixmap_signal = pyqtSignal(np.ndarray, np.ndarray, bool, str)
    
    def __init__(self, reference_poses, tolerance=ANGLE_TOLERANCE):
        super().__init__()
        self._run_flag = True
        self.reference_poses = reference_poses
        self.tolerance = tolerance
        self.current_pose_index = 0
        self.total_poses = len(reference_poses)
    
    def run(self):
        # Canlı kamera akışını başlat
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Webcam açılmadı.")
            self._run_flag = False
        
        while self._run_flag and self.current_pose_index < self.total_poses:
            ret, frame = cap.read()
            if not ret:
                print("Kamera okunamadı.")
                break
            
            # Frame'i yatay olarak çevir (ayna görüntüsünü önlemek için)
            frame = cv2.flip(frame, 1)
            
            # BGR'den RGB'ye dönüştür
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Mediapipe ile poz işlemi
            pose_results = pose.process(rgb_frame)
            
            # Eklemler ve bağlantılar çizme (sadece canlı görüntü için)
            if pose_results.pose_landmarks:
                landmarks = pose_results.pose_landmarks.landmark
                image_height, image_width, _ = frame.shape
                
                # Pose landmarklarını çiz
                annotated_live_frame = annotate_image(frame.copy(), pose_results.pose_landmarks, image_width, image_height)
                
                # Açıları hesapla
                current_angles = get_pose_angles(landmarks, image_width, image_height)
                
                # Poz kontrolü
                reference_pose = self.reference_poses[self.current_pose_index]
                reference_angles = reference_pose['angles']
                reference_image = reference_pose['annotated_image']
                
                # Referans resmini yeniden boyutlandır (live frame ile aynı yüksekliğe)
                ref_height, ref_width, _ = reference_image.shape
                scale_ratio = image_height / ref_height
                new_ref_width = int(ref_width * scale_ratio)
                resized_reference = cv2.resize(reference_image, (new_ref_width, image_height))
                
                # Poz kontrolü
                is_correct_pose = compare_angles(reference_angles, current_angles, self.tolerance)
                
                # Referans pozun adını al
                reference_name = reference_pose['name']
                
                # Sonuçları göstermek için sinyal gönder
                self.change_pixmap_signal.emit(resized_reference, annotated_live_frame, is_correct_pose, reference_name)
                
                # 30 FPS için küçük bir gecikme ekleyin
                time.sleep(1/30)
            else:
                # Poz bulunamadığında siyah referans görüntüsü gönder
                blank_ref = np.zeros_like(frame)
                self.change_pixmap_signal.emit(blank_ref, frame, False, "Poz Bulunamadı")
                time.sleep(1/30)
        
        # Kaynakları serbest bırak
        cap.release()
    
    def stop(self):
        """Thread'i durdurur."""
        self._run_flag = False
        self.wait()



from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QSpacerItem , QSizePolicy , QWidget
import sys
import cv2
import os
from PyQt5.QtCore import Qt
import subprocess

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setWindowTitle("Poz Tespit Uygulaması")
        self.disply_width = 640
        self.display_height = 480

        # Arka plan rengi ayarları
        Form.setStyleSheet("background-color: lightblue;")  # Arka plan rengi

        # Video akışını göstermek için QLabel
        self.image_label = QLabel(Form)
        self.image_label.resize(self.disply_width, self.display_height)

        # Referans poz görüntüsünü göstermek için QLabel
        self.reference_label = QLabel(Form)
        self.reference_label.resize(self.disply_width, self.display_height)

        # Durum mesajını göstermek için QLabel
        self.status_label = QLabel(Form)
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("font-size: 16px; color: green;")

        # 'Sonraki', 'Önceki', 'Durdur' ve 'Yeniden Başlat' butonları
        self.next_button = QPushButton("Sonraki", Form)
        self.next_button.setFixedSize(100, 50)
        self.next_button.setStyleSheet("background-color: lightgreen; color: black;")  # Renk ayarları

        self.previous_button = QPushButton("Önceki", Form)
        self.previous_button.setFixedSize(100, 50)
        self.previous_button.setStyleSheet("background-color: lightcoral; color: white;")  # Renk ayarları

        self.stop_button = QPushButton("Durdur", Form)
        self.stop_button.setFixedSize(100, 50)
        self.stop_button.setStyleSheet("background-color: orange; color: black;")  # Renk ayarları

        self.restart_button = QPushButton("Yeniden Başlat", Form)
        self.restart_button.setFixedSize(150, 50)
        self.restart_button.setStyleSheet("background-color: royalblue; color: white;")  # Renk ayarları

        self.b_back = QPushButton("Geri Dön ", Form)
        self.b_back.setFixedSize(100, 40) 
        self.b_back.setStyleSheet("background-color: darkgray; color: white;")  # Renk ayarları

        # Butonları bir araya getirmek için horizontal layout
        button_hbox = QHBoxLayout()
        button_hbox.addWidget(self.previous_button)
        button_hbox.addWidget(self.next_button)
        button_hbox.addWidget(self.stop_button)
        button_hbox.addWidget(self.restart_button)

        # Boşluklar (spacers) ekleyerek yerleşim düzenini ayarlıyoruz
        spacer_above_buttons = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)  # Butonların üstüne boşluk
        spacer_below_buttons = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)  # Butonların altına boşluk
        spacer_below_labels = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)  # Label'ların altına boşluk

        # Layout ayarlamaları
        hbox = QHBoxLayout()
        hbox.addWidget(self.image_label)
        hbox.addWidget(self.reference_label)

        vbox = QVBoxLayout()
        vbox.addWidget(self.b_back)  # Geri butonunu üstte ekliyoruz
        vbox.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))  # Geri butonunun altına boşluk ekliyoruz
        vbox.addSpacerItem(spacer_below_labels)  # Label'ları aşağı kaydırmak için altına boşluk ekliyoruz
        vbox.addLayout(hbox)
        vbox.addWidget(self.status_label)
        vbox.addSpacerItem(spacer_above_buttons)  # Butonları yukarı taşımak için üstlerine boşluk ekliyoruz
        vbox.addLayout(button_hbox)  # Butonlar layout'u
        vbox.addSpacerItem(spacer_below_buttons)  # Butonların altına boşluk ekliyoruz

        Form.setLayout(vbox)




class MainWindow(QWidget):
    
    def __init__(self, reference_poses, tolerance=ANGLE_TOLERANCE):
        super().__init__()
    
        # UI'yi başlat
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.show()
        # Video thread başlat
        self.thread = VideoThread(reference_poses, tolerance)
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.start()
        
        # Poz kontrol flag
        self.skip_current_pose = False
        
        # Pose işleme flag
        self.pose_handled = False

        
        # Buton eventleri
        self.ui.next_button.clicked.connect(self.next_pose)
        self.ui.previous_button.clicked.connect(self.previous_pose)
        self.ui.stop_button.clicked.connect(self.stop_thread)
        self.ui.restart_button.clicked.connect(self.restart_thread)
        self.ui.b_back.clicked.connect(self.go_back)

    def go_back(self):
        subprocess.Popen([sys.executable, "start_menu.py"])
        #self.close()
        


    def closeEvent(self, event):
        """Uygulama kapatılırken thread'i durdurur."""
        self.thread.stop()
        event.accept()
    
    def next_pose(self):
        """Kullanıcı 'Sonraki' butonuna bastığında bir sonraki pozu atlar."""
        self.skip_current_pose = True
    
    def previous_pose(self):
        """Kullanıcı 'Önceki' butonuna bastığında bir önceki poza geçer."""
        if self.thread.current_pose_index > 0:
            self.thread.current_pose_index -= 1
            self.pose_handled = False
            self.skip_current_pose = False
            self.ui.status_label.setText("Bir önceki poz yüklendi.")
            self.ui.status_label.setStyleSheet("font-size: 16px; color: green;")
        else:
            self.ui.status_label.setText("Zaten ilk pozdasınız.")
            self.ui.status_label.setStyleSheet("font-size: 16px; color: red;")
    
    def stop_thread(self):
        """Durdur butonuna basıldığında thread'i durdurur."""
        self.thread.stop()
        self.ui.status_label.setText("Video Durduruldu.")
        self.ui.status_label.setStyleSheet("font-size: 16px; color: red;")
    
    def restart_thread(self):
        """Yeniden Başlat butonuna basıldığında thread'i yeniden başlatır."""
        # Mevcut thread'i durdur
        self.thread.stop()
        
        # Poz indeksini sıfırla
        self.thread.current_pose_index = 0
        
        # Pose işleme flag'ını sıfırla
        self.pose_handled = False
        self.skip_current_pose = False
        
        # Durum mesajını güncelle
        self.ui.status_label.setText("Video Yeniden Başlatıldı.")
        self.ui.status_label.setStyleSheet("font-size: 16px; color: green;")
        
        # Yeni bir thread oluştur ve başlat
        self.thread = VideoThread(self.thread.reference_poses, self.thread.tolerance)
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.start()
    
    def update_image(self, reference_image, live_frame, is_correct_pose, reference_name):
        """Video thread'den gelen sinyalleri alır ve GUI'yi günceller."""
        if live_frame is not None:
            qt_live_image = self.convert_cv_qt(live_frame)
            self.ui.image_label.setPixmap(qt_live_image)
        
        if reference_image is not None:
            qt_ref_image = self.convert_cv_qt(reference_image)
            self.ui.reference_label.setPixmap(qt_ref_image)
        
        if (is_correct_pose or self.skip_current_pose) and not self.pose_handled:
            if is_correct_pose:
                status_text = f"Poz '{reference_name}' başarıyla tamamlandı."
                status_color = "green"
            else:
                status_text = f"Poz '{reference_name}' atlandı."
                status_color = "red"
            
            self.ui.status_label.setText(status_text)
            self.ui.status_label.setStyleSheet(f"font-size: 16px; color: {status_color};")
            self.thread.current_pose_index += 1
            self.pose_handled = True
            
            if self.skip_current_pose:
                self.skip_current_pose = False
            
            if self.thread.current_pose_index >= self.thread.total_poses:
                self.ui.status_label.setText("Tüm pozlar tamamlandı.")
                self.ui.status_label.setStyleSheet("font-size: 16px; color: green;")
                self.thread.stop()
            else:
                self.pose_handled = False
                next_pose_name = self.thread.reference_poses[self.thread.current_pose_index]['name']
                print(f"Poz {self.thread.current_pose_index + 1} ({next_pose_name}) yüklendi.")
    
    def convert_cv_qt(self, cv_img):
        """OpenCV görüntüsünü QImage formatına dönüştürür."""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.ui.disply_width, self.ui.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

# Main fonksiyonu burada
def main():
    
    input_directory = "hareketler"

    if not os.path.exists(input_directory):
        print(f"Giriş klasörü bulunamadı: {input_directory}")
        sys.exit(1)
    
    reference_poses = process_reference_images(input_directory)
    
    if not reference_poses:
        print("Hiçbir referans resim bulunamadı. Program sonlandırılıyor.")
        sys.exit(1)
    
    app = QApplication(sys.argv)
    window = MainWindow(reference_poses, tolerance=ANGLE_TOLERANCE)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
