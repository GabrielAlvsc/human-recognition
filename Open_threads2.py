import cv2
from ultralytics import YOLO
import threading
import time

# Carregar o modelo YOLO
model = YOLO("yolo-Weights/yolov8n.pt")

# Definições das câmeras
cameras = {
    "Camera1": "rtsp://kafn:fa6nca@192.168.218.181:554/onvif1?overrun_nonfatal=1&fifo_size=50000000",
    "Camera2": "rtsp://udne:aa4tru@192.168.218.252:554/onvif2?overrun_nonfatal=1&fifo_size=50000000"
}

# Dicionário para contar detecções de humanos por câmera
human_detections = {camera: 0 for camera in cameras}

def process_camera(url, camera_name):
    cap = cv2.VideoCapture(url, cv2.CAP_FFMPEG)
    
    if not cap.isOpened():
        print(f"Erro ao abrir a câmera {camera_name}")
        return
    
    try:
        while True:
            start_time = time.time()

            ret, frame = cap.read()
            if not ret:
                print(f"Frame não foi recebido corretamente em {camera_name}")
                continue

            # Detecção usando YOLO
            results = model(frame, stream=True)
            human_detected = False
            
            # Desenho das caixas delimitadoras e verificação de detecções humanas
            for r in results:
                boxes = r.boxes
                for box in boxes:
                    c = box.cls
                    class_name = model.names[int(c)]
                    if class_name == 'person':
                        human_detected = True
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 255), 3)

            if human_detected:
                human_detections[camera_name] += 1
            else:
                human_detections[camera_name] = 0  # Reset se não houver detecção consecutiva

            cv2.imshow(f'VIDEO {camera_name}', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            # Parar se duas detecções consecutivas forem encontradas
            if human_detections[camera_name] >= 2:
                print(f"Duas detecções consecutivas de humanos em {camera_name}. Parando.")
                break

            # Manter a taxa de 30 FPS
            frame_time = time.time() - start_time
            if frame_time < 1.0 / 30:
                time.sleep(1.0 / 30 - frame_time)

    finally:
        cap.release()
        cv2.destroyAllWindows()

threads = []
for name, url in cameras.items():
    t = threading.Thread(target=process_camera, args=(url, name))
    t.start()
    threads.append(t)

# Aguardar todas as threads terminarem
for t in threads:
    t.join()
