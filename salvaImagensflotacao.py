# import cv2
# import time
# import os
# import threading

# def capturar_camera(url, pasta_destino, nome_camera):
#     os.makedirs(pasta_destino, exist_ok=True)
#     cap = cv2.VideoCapture(url)

#     if not cap.isOpened():
#         print(f"[{nome_camera}] Não foi possível abrir o stream: {url}")
#         return

#     while True:
#         ret, frame = cap.read()
#         if ret:
#             print(f"[{nome_camera}] Tamanho do frame:", frame.shape)
#             timestamp = time.strftime("%Y%m%d-%H%M%S")
#             filename = os.path.join(pasta_destino, f"frame_{timestamp}.jpg")
#             cv2.imwrite(filename, frame)
#             print(f"[{nome_camera}] Frame salvo: {filename}")
#         else:
#             print(f"[{nome_camera}] Erro ao capturar frame.")

#         time.sleep(20)

# # === Câmera 1 ===
# url1 = "http://{ip_camara1}/mjpg/video.mjpg?resolution=640x480&quality=100"
# pasta1 = r"C:\Aplicação CEMI\Flotação TO\MF641102"

# # === Câmera 2 ===
# url2 = "http://{ip_camara2}/mjpg/video.mjpg?resolution=640x480&quality=100"
# pasta2 = r"C:\Aplicação CEMI\Flotação TO\MF641202"

# # === Criar e iniciar as threads ===
# thread1 = threading.Thread(target=capturar_camera, args=(url1, pasta1, "CAM1"))
# thread2 = threading.Thread(target=capturar_camera, args=(url2, pasta2, "CAM2"))

# thread1.start()
# thread2.start()

# # Espera ambas as threads (opcional, bloqueia o terminal)
# thread1.join()
# thread2.join()
# print("Todas as threads foram concluídas.")

import cv2
import time
import os
import threading
from datetime import datetime

def capturar_camera(url, pasta_destino, nome_camera, intervalo=20, stop_event=None, reconnect_delay=5):
    """
    Lê 1 frame a cada `intervalo` segundos e salva em `pasta_destino`.
    Tenta reconectar se o stream cair.
    """
    os.makedirs(pasta_destino, exist_ok=True)
    if stop_event is None:
        stop_event = threading.Event()

    while not stop_event.is_set():
        cap = cv2.VideoCapture(url)

        # (Opcional) reduzir latência de buffer, se o backend suportar
        try:
            cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        except Exception:
            pass

        if not cap.isOpened():
            print(f"[{nome_camera}] Não foi possível abrir o stream. Nova tentativa em {reconnect_delay}s: {url}")
            time.sleep(reconnect_delay)
            continue

        print(f"[{nome_camera}] Conectado.")
        try:
            while not stop_event.is_set():
                ret, frame = cap.read()
                if not ret or frame is None:
                    print(f"[{nome_camera}] Falha ao ler frame. Tentando reconectar em {reconnect_delay}s…")
                    time.sleep(reconnect_delay)
                    break  # sai do loop interno para recriar o VideoCapture

                # timestamp com milissegundos para evitar colisão de nomes
                ts = datetime.now().strftime("%Y%m%d-%H%M%S-%f")[:-3]
                filename = os.path.join(pasta_destino, f"{nome_camera}_frame_{ts}.jpg")
                ok = cv2.imwrite(filename, frame)
                if ok:
                    print(f"[{nome_camera}] Frame salvo: {filename} (shape: {frame.shape})")
                else:
                    print(f"[{nome_camera}] Erro ao salvar frame em disco.")

                # aguarda até a próxima captura
                for _ in range(intervalo * 10):  # checa stop_event com granularidade de 0,1s
                    if stop_event.is_set():
                        break
                    time.sleep(0.1)
        finally:
            cap.release()
            print(f"[{nome_camera}] Conexão fechada.")

# ===================== CONFIGURAÇÃO DAS CÂMERAS =====================

# Preencha os IPs reais das câmeras:
url1 = "http://10.7.19.154/mjpg/video.mjpg?resolution=640x480&quality=100"
url2 = "http://10.7.19.160/mjpg/video.mjpg?resolution=640x480&quality=100"
url3 = "http://10.7.19.153/mjpg/video.mjpg?resolution=640x480&quality=100"
url4 = "http://10.7.19.158/mjpg/video.mjpg?resolution=640x480&quality=100"

# Pastas de destino (Windows: use r"…"):
pasta1 = r"C:\Aplicação CEMI\Flotação TO\MF641102"
pasta2 = r"C:\Aplicação CEMI\Flotação TO\MF641202"
pasta3 = r"C:\Aplicação CEMI\Flotação TO\MF641101"
pasta4 = r"C:\Aplicação CEMI\Flotação TO\MF641201"

# Monte a lista: (url, pasta, nome)
cameras = [
    (url1, pasta1, "CAM1"),
    (url2, pasta2, "CAM2"),
    (url3, pasta3, "CAM3"),
    (url4, pasta4, "CAM4"),
]

# Intervalo entre capturas (segundos) – ajuste se quiser
INTERVALO = 3600  # 3600s = 1 hora

# ===================== INICIALIZAÇÃO =====================

stop_event = threading.Event()
threads = []

for url, pasta, nome in cameras:
    t = threading.Thread(
        target=capturar_camera,
        args=(url, pasta, nome, INTERVALO, stop_event),
        daemon=True
    )
    t.start()
    threads.append(t)

print(f"Iniciadas {len(threads)} threads de captura.")

try:
    # Mantém a main viva enquanto as threads trabalham
    while any(t.is_alive() for t in threads):
        time.sleep(1)
except KeyboardInterrupt:
    print("Recebido Ctrl+C. Encerrando…")
finally:
    stop_event.set()
    for t in threads:
        t.join()

print("Todas as threads foram concluídas.")
