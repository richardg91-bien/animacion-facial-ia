#!/usr/bin/env python3
"""
animacion_interactiva.py
Script integrado con GUI para cartoonizar imágenes y animar labios.
- Usa MediaPipe para detectar landmarks faciales (labios).
- Genera voz offline con pyttsx3.
- Si existe un script wav2lip_mejorado.py en la carpeta 'extras' intenta usarlo para mejor sincronía (opcional).
- Combina audio y video con ffmpeg si está disponible.

Cómo usar:
1) Coloca este script en la misma carpeta que tus recursos o usa el botón "Seleccionar imagen".
2) Instala dependencias: pip install opencv-python mediapipe numpy pyttsx3
3) (Opcional) Instala ffmpeg para combinar audio y video.
"""

import os
import sys
import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import subprocess
import pyttsx3
import mediapipe as mp

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXTRAS_DIR = os.path.join(BASE_DIR, "extras")

# MediaPipe setup
mp_face_mesh = mp.solutions.face_mesh

def cartoonify_image(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)
    edges = cv2.adaptiveThreshold(gray, 255,
                                  cv2.ADAPTIVE_THRESH_MEAN_C,
                                  cv2.THRESH_BINARY, 9, 9)
    color = cv2.bilateralFilter(img, 9, 250, 250)
    cartoon = cv2.bitwise_and(color, color, mask=edges)
    return cartoon

def generar_voz(texto, salida_mp3):
    engine = pyttsx3.init()
    # Ajustes de voz (opcionales)
    try:
        engine.setProperty('rate', 150)
    except Exception:
        pass
    engine.save_to_file(texto, salida_mp3)
    engine.runAndWait()

def detectar_labios_mediapipe(imagen):
    with mp_face_mesh.FaceMesh(static_image_mode=True, refine_landmarks=True) as face_mesh:
        img_rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
        res = face_mesh.process(img_rgb)
        if not res.multi_face_landmarks:
            return None
        lm = res.multi_face_landmarks[0]
        h, w, _ = imagen.shape
        indices = list(range(61, 88))  # región de labios en MediaPipe
        puntos = []
        for idx in indices:
            l = lm.landmark[idx]
            puntos.append((int(l.x * w), int(l.y * h)))
        return np.array(puntos, np.int32)

def animar_labios_simple(imagen, puntos_labios, salida_avi, fps=20, frames_count=30):
    h, w, _ = imagen.shape
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(salida_avi, fourcc, fps, (w, h))
    # Generar frames con apertura de labios variable
    for i in range(frames_count):
        frame = imagen.copy()
        apertura = abs((i % (frames_count//3)) - (frames_count//6)) / max(1, (frames_count//6)) * 12
        puntos_mod = puntos_labios.copy()
        for j in range(len(puntos_mod)):
            # mitad superior -> sube un poco; inferior -> baja más
            if j > len(puntos_mod)//2:
                puntos_mod[j][1] += int(apertura)
            else:
                puntos_mod[j][1] -= int(apertura/2)
        cv2.fillPoly(frame, [puntos_mod], (0,0,0))
        out.write(frame)
    out.release()

def usar_wav2lip_externo(image_path, audio_path, output_path):
    """
    Si existe un script wav2lip_mejorado.py en extras, lo intentamos usar.
    El script externo debe aceptar parámetros (imagen, audio, salida) o adaptarlo aquí.
    """
    script_path = os.path.join(EXTRAS_DIR, "wav2lip_mejorado.py")
    if not os.path.exists(script_path):
        return False, "No hay script wav2lip_mejorado.py en extras."
    # Llamada simple: python extras/wav2lip_mejorado.py --image X --audio Y --out Z
    cmd = [sys.executable, script_path, "--image", image_path, "--audio", audio_path, "--out", output_path]
    try:
        proc = subprocess.run(cmd, cwd=EXTRAS_DIR, capture_output=True, text=True, timeout=300)
        if proc.returncode == 0 and os.path.exists(output_path):
            return True, "Wav2Lip producido correctamente."
        else:
            return False, f"Wav2Lip falló. stdout/stderr:\\n{proc.stdout}\\n{proc.stderr}"
    except Exception as e:
        return False, str(e)

def combinar_audio_video(ffmpeg_path, video_path, audio_path, salida_final):
    if not os.path.exists(video_path) or not os.path.exists(audio_path):
        return False, "Falta video o audio."
    cmd = [ffmpeg_path, "-y", "-i", video_path, "-i", audio_path, "-shortest", "-c:v", "copy", "-c:a", "aac", salida_final]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if proc.returncode == 0 and os.path.exists(salida_final):
            return True, "Combinación correcta."
        else:
            return False, proc.stderr + "\\n" + proc.stdout
    except Exception as e:
        return False, str(e)

# ---------------- GUI ----------------
class App:
    def __init__(self, root):
        self.root = root
        root.title("Animación Interactiva - Cartoon + Labios")
        root.geometry("520x300")
        self.imagen_path = None

        frm = tk.Frame(root, padx=10, pady=10)
        frm.pack(fill=tk.BOTH, expand=True)

        tk.Label(frm, text="1) Selecciona una imagen (cara)").grid(row=0, column=0, sticky="w")
        btn = tk.Button(frm, text="Seleccionar imagen", command=self.seleccionar_imagen)
        btn.grid(row=0, column=1, sticky="w")

        tk.Label(frm, text="2) Texto a decir:").grid(row=1, column=0, sticky="w", pady=(10,0))
        self.texto_entry = tk.Entry(frm, width=40)
        self.texto_entry.grid(row=1, column=1, sticky="w", pady=(10,0))
        self.texto_entry.insert(0, "Hola, soy...")

        tk.Label(frm, text="3) Nombre de salida:").grid(row=2, column=0, sticky="w", pady=(10,0))
        self.salida_entry = tk.Entry(frm, width=40)
        self.salida_entry.grid(row=2, column=1, sticky="w", pady=(10,0))
        self.salida_entry.insert(0, "salida")

        self.use_wav2lip_var = tk.IntVar()
        cb = tk.Checkbutton(frm, text="Usar Wav2Lip externo si está disponible (extras/wav2lip_mejorado.py)", variable=self.use_wav2lip_var)
        cb.grid(row=3, column=0, columnspan=2, pady=(10,0), sticky="w")

        self.status = tk.Label(frm, text="Estado: listo", anchor="w", justify="left")
        self.status.grid(row=4, column=0, columnspan=2, sticky="we", pady=(15,0))

        gen_btn = tk.Button(frm, text="Generar animación", command=self.on_generar)
        gen_btn.grid(row=5, column=0, columnspan=2, pady=(15,0))

    def seleccionar_imagen(self):
        path = filedialog.askopenfilename(filetypes=[("Images","*.jpg *.jpeg *.png")])
        if path:
            self.imagen_path = path
            self.status.config(text=f"Imagen seleccionada: {os.path.basename(path)}")

    def on_generar(self):
        if not self.imagen_path:
            messagebox.showwarning("Error", "Selecciona primero una imagen.")
            return
        texto = self.texto_entry.get().strip()
        nombre = self.salida_entry.get().strip() or "salida"
        threading.Thread(target=self.procesar, args=(self.imagen_path, texto, nombre), daemon=True).start()

    def procesar(self, imagen_path, texto, nombre_salida):
        try:
            self.status.config(text="Estado: cargando imagen...")
            img = cv2.imread(imagen_path)
            if img is None:
                self.status.config(text="Error: no se pudo abrir la imagen.")
                return
            self.status.config(text="Estado: cartoonizando...")
            cartoon = cartoonify_image(img)
            out_dir = os.path.join(BASE_DIR, "resultados")
            os.makedirs(out_dir, exist_ok=True)
            cartoon_path = os.path.join(out_dir, f"{nombre_salida}_cartoon.jpg")
            cv2.imwrite(cartoon_path, cartoon)

            self.status.config(text="Estado: detectando labios...")
            puntos = detectar_labios_mediapipe(cartoon)
            if puntos is None:
                self.status.config(text="No se detectó rostro/labios. Intenta otra foto.")
                return

            self.status.config(text="Estado: generando audio...")
            audio_path = os.path.join(out_dir, f"{nombre_salida}.mp3")
            generar_voz(texto, audio_path)

            # Primero intentamos Wav2Lip si el usuario lo pidió
            video_path = os.path.join(out_dir, f"{nombre_salida}.avi")
            final_path = os.path.join(out_dir, f"{nombre_salida}_final.mp4")
            used_wav2lip = False
            if self.use_wav2lip_var.get():
                self.status.config(text="Estado: intentando Wav2Lip externo (si existe)...")
                success, msg = usar_wav2lip_externo(imagen_path, audio_path, final_path)
                if success:
                    self.status.config(text=f"Wav2Lip OK. Guardado: {final_path}")
                    used_wav2lip = True
                else:
                    # continuar con fallback
                    self.status.config(text=f"Wav2Lip no disponible o falló, usando fallback. {msg}")

            if not used_wav2lip:
                self.status.config(text="Estado: animando labios (fallback Mediapipe)...")
                animar_labios_simple(cartoon, puntos, video_path, fps=20, frames_count=30)
                # intentar combinar con ffmpeg (si está instalado)
                ffmpeg_path = shutil.which("ffmpeg") or "ffmpeg"
                if shutil.which("ffmpeg"):
                    ok, msg = combinar_audio_video(ffmpeg_path, video_path, audio_path, final_path)
                    if ok:
                        self.status.config(text=f"Combinación completada: {final_path}")
                    else:
                        self.status.config(text=f"Video creado: {video_path} (ffmpeg falló: {msg})")
                else:
                    self.status.config(text=f"Video creado: {video_path} (instala ffmpeg para combinar audio)")

            messagebox.showinfo("Listo", f"Proceso terminado.\nResultados en: {os.path.join(BASE_DIR, 'resultados')}")
            self.status.config(text="Estado: listo")
        except Exception as e:
            self.status.config(text=f"Error: {str(e)}")
            import traceback; traceback.print_exc()

if __name__ == '__main__':
    import shutil
    root = tk.Tk()
    app = App(root)
    root.mainloop()
