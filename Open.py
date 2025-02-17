import cv2
import psycopg2
import threading
import time
from tkinter import Tk, Label, Entry, Button
from ultralytics import YOLO  # A biblioteca fictícia do YOLO
from Sms import fetch_and_send_messages  # Função fictícia para enviar mensagens

# Conexão com o banco de dados PostgreSQL
conn = psycopg2.connect(
    dbname="mydatabase",
    user="postgres",
    password="engcomp1413",
    host="localhost",
    port="5432"
)
conn.autocommit = True
cursor = conn.cursor()

# Carregar o modelo YOLO
model = YOLO("yolo-Weights/yolov8n.pt")

# Definições das câmeras
cameras = {
    "Camera1": "rtsp://kafn:fa6nca@192.168.150.181:554/onvif1?overrun_nonfatal=1&fifo_size=50000000",
    "Camera2": "rtsp://udne:aa4tru@192.168.150.253:554/onvif2?overrun_nonfatal=1&fifo_size=50000000"
}

stop_event = threading.Event()
# Dicionário para contar detecções de humanos por câmera
human_detections = {camera: 0 for camera in cameras}
permissiontosend = {camera: 0 for camera in cameras}

# Função para processar cada câmera
def process_camera(url, camera_name):
    
    cap = cv2.VideoCapture(url, cv2.CAP_FFMPEG)
    if not cap.isOpened():
        print(f"Erro ao abrir a câmera {camera_name}")
        return

    try:
        while True:
            print(camera_name)
            start_time = time.time()
            ret, frame = cap.read()
            if not ret:
                print(f"Frame não foi recebido corretamente em {camera_name}")
                continue

            results = model(frame, stream=True)  # Detecção com YOLO
            human_detected = False
            for r in results:
                boxes = r.boxes
                for box in boxes:
                    class_name = model.names[int(box.cls)]
                    if class_name == 'person':
                        human_detected = True
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 255), 3)

            if human_detected:
                human_detections[camera_name] += 1
            else:
                human_detections[camera_name] = 0
                permissiontosend[camera_name] = 1

            print(human_detections[camera_name])
            print(permissiontosend[camera_name])
            cv2.imshow(f'VIDEO {camera_name}', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            if (human_detections[camera_name] >= 2) and (permissiontosend[camera_name] == 1):
                permissiontosend[camera_name] = 0
                
                print(f"Duas detecções consecutivas de humanos em {camera_name}. Enviando mensagem.")

                fetch_and_send_messages(camera_name)
                r.show() 
                continue

            frame_time = time.time() - start_time
            if frame_time < 1.0 / 30:
                time.sleep(1.0 / 30 - frame_time)

    finally:
        cap.release()
        cv2.destroyAllWindows()



# Função que inicia a thread para cada câmera

threads = []
for name, url in cameras.items():
    t = threading.Thread(target=process_camera, args=(url, name))
    t.start()
    threads.append(t)
    # Aguardar todas as threads terminarem
for t in threads:
    t.join()