import cv2
import mediapipe as mp
import time
import numpy as np
from pygame import mixer
import os

# Inicializar pygame mixer
mixer.init()

# Cargar sonido de alerta (usa formato .wav mejor)
alert_path = 'alerta.wav'
if not os.path.exists(alert_path):
    raise FileNotFoundError(f"No se encontró el archivo '{alert_path}'")

alert_sound = mixer.Sound(alert_path)

# Inicializar MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Constantes
EYE_AR_THRESH = 0.25
EYE_CLOSED_SECONDS = 3

def eye_aspect_ratio(eye_landmarks, landmarks, frame_shape):
    p1 = np.array([landmarks[eye_landmarks[0]].x * frame_shape[1], landmarks[eye_landmarks[0]].y * frame_shape[0]])
    p2 = np.array([landmarks[eye_landmarks[1]].x * frame_shape[1], landmarks[eye_landmarks[1]].y * frame_shape[0]])
    p3 = np.array([landmarks[eye_landmarks[2]].x * frame_shape[1], landmarks[eye_landmarks[2]].y * frame_shape[0]])
    p4 = np.array([landmarks[eye_landmarks[3]].x * frame_shape[1], landmarks[eye_landmarks[3]].y * frame_shape[0]])

    vert_dist1 = np.linalg.norm(p3 - p4)
    horz_dist = np.linalg.norm(p1 - p2)

    ear = vert_dist1 / horz_dist if horz_dist != 0 else 0
    return ear

cap = cv2.VideoCapture(0)
closed_eye_start = None
eyes_closed = False
alarm_triggered = False

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(frame_rgb)
    frame = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            landmarks = face_landmarks.landmark
            frame_shape = frame.shape

            left_eye_ear = eye_aspect_ratio([33, 133, 159, 145], landmarks, frame_shape)
            right_eye_ear = eye_aspect_ratio([362, 263, 386, 374], landmarks, frame_shape)
            ear = (left_eye_ear + right_eye_ear) / 2.0

            for idx in [33, 133, 159, 145, 362, 263, 386, 374]:
                lm = landmarks[idx]
                x, y = int(lm.x * frame_shape[1]), int(lm.y * frame_shape[0])
                cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

            if ear < EYE_AR_THRESH:
                if not eyes_closed:
                    closed_eye_start = time.time()
                    eyes_closed = True
                elif time.time() - closed_eye_start >= EYE_CLOSED_SECONDS:
                    cv2.putText(frame, "ALERTA: Durmiendo!", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    if not alarm_triggered:
                        alert_sound.play()
                        alarm_triggered = True
            else:
                eyes_closed = False
                closed_eye_start = None
                alarm_triggered = False
                alert_sound.stop()  # Detener sonido si vuelve a abrir los ojos

            cv2.putText(frame, f"EAR: {ear:.2f}", (300, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

    cv2.imshow("Drowsiness Detector", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
face_mesh.close()
