import cv2
import time
import os
import threading

def capturar_camera(url, pasta_destino, nome_camera):
    os.makedirs(pasta_destino, exist_ok=True)
    cap = cv2.VideoCapture(url)

    if not cap.isOpened():
        print(f"[{nome_camera}] Não foi possível abrir o stream: {url}")
        return

    while True:
        ret, frame = cap.read()
        if ret:
            print(f"[{nome_camera}] Tamanho do frame:", frame.shape)
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            filename = os.path.join(pasta_destino, f"frame_{timestamp}.jpg")
            cv2.imwrite(filename, frame)
            print(f"[{nome_camera}] Frame salvo: {filename}")
        else:
            print(f"[{nome_camera}] Erro ao capturar frame.")

        time.sleep(20)

# === Câmera 1 ===
url1 = "http://{ip_camara1}/mjpg/video.mjpg?resolution=640x480&quality=100"
pasta1 = r"C:\Aplicação CEMI\Flotação TO\MF641102"

# === Câmera 2 ===
url2 = "http://{ip_camara2}/mjpg/video.mjpg?resolution=640x480&quality=100"
pasta2 = r"C:\Aplicação CEMI\Flotação TO\MF641202"

# === Criar e iniciar as threads ===
thread1 = threading.Thread(target=capturar_camera, args=(url1, pasta1, "CAM1"))
thread2 = threading.Thread(target=capturar_camera, args=(url2, pasta2, "CAM2"))

thread1.start()
thread2.start()

# Espera ambas as threads (opcional, bloqueia o terminal)
thread1.join()
thread2.join()
print("Todas as threads foram concluídas.")