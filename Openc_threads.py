import cv2
from ultralytics import YOLO
import threading
import time

# Carregar o modelo YOLO
model = YOLO("yolo-Weights/yolov8n.pt")

# Definições das câmeras
cameras = {
    "Camera1": "rtsp://Honor:Mateus2449@192.168.100.158:554/onvif1?overrun_nonfatal=1&fifo_size=50000000",
    "Camera2": "rtsp://udne:en4t75@192.168.100.216:554/onvif2?overrun_nonfatal=1&fifo_size=50000000"
}


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
                continue  # Em vez de quebrar, continua tentando

            # Detecção usando YOLO
            results = model(frame, stream=True)
            print({camera_name})
            # Desenho das caixas delimitadoras baseadas nas detecções de YOLO
            for r in results:
                print(r)
                boxes = r.boxes
                for box in boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 255), 3)
                 

            cv2.imshow(f'VIDEO {camera_name}', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
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
