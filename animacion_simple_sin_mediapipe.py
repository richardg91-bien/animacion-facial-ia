#!/usr/bin/env python3
"""
Versión simplificada sin MediaPipe para evitar problemas de compatibilidad
Solo usa OpenCV para detección básica de caras y pyttsx3 para audio
"""
import os
import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import subprocess
import pyttsx3

def cartoonify_image(img):
    """Aplicar filtro cartoon a la imagen"""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)
    edges = cv2.adaptiveThreshold(gray, 255,
                                  cv2.ADAPTIVE_THRESH_MEAN_C,
                                  cv2.THRESH_BINARY, 9, 9)
    color = cv2.bilateralFilter(img, 9, 250, 250)
    cartoon = cv2.bitwise_and(color, color, mask=edges)
    return cartoon

def generar_voz(texto, salida_wav):
    """Generar audio desde texto"""
    engine = pyttsx3.init()
    try:
        engine.setProperty('rate', 150)
    except Exception:
        pass
    engine.save_to_file(texto, salida_wav)
    engine.runAndWait()
    return salida_wav

def detectar_cara_simple(imagen):
    """Detectar cara usando OpenCV básico"""
    try:
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        if len(faces) > 0:
            # Tomar la cara más grande
            face = max(faces, key=lambda x: x[2] * x[3])
            x, y, w, h = face
            
            # Simular región de labios (tercio inferior de la cara)
            mouth_y = y + int(h * 0.6)
            mouth_h = int(h * 0.4)
            mouth_x = x + int(w * 0.2)
            mouth_w = int(w * 0.6)
            
            # Crear puntos aproximados de labios
            puntos_labios = np.array([
                [mouth_x, mouth_y + mouth_h//3],
                [mouth_x + mouth_w//4, mouth_y],
                [mouth_x + mouth_w//2, mouth_y],
                [mouth_x + 3*mouth_w//4, mouth_y],
                [mouth_x + mouth_w, mouth_y + mouth_h//3],
                [mouth_x + 3*mouth_w//4, mouth_y + 2*mouth_h//3],
                [mouth_x + mouth_w//2, mouth_y + mouth_h],
                [mouth_x + mouth_w//4, mouth_y + 2*mouth_h//3]
            ], np.int32)
            
            return puntos_labios, (x, y, w, h)  # Devolver también coordenadas de cara
        return None, None
    except Exception as e:
        print(f"Error en detección de cara: {e}")
        return None, None

def animar_labios_simple(imagen, puntos_labios, salida_avi, fps=25, frames_count=40):
    """Crear animación simple de labios"""
    h, w, _ = imagen.shape
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(salida_avi, fourcc, fps, (w, h))
    
    for i in range(frames_count):
        frame = imagen.copy()
        
        # Variar la apertura de labios
        apertura = abs((i % (frames_count//3)) - (frames_count//6)) / max(1, (frames_count//6)) * 8
        
        # Modificar puntos para simular habla
        puntos_mod = puntos_labios.copy()
        for j in range(len(puntos_mod)):
            if j > len(puntos_mod)//2:  # Puntos inferiores
                puntos_mod[j][1] += int(apertura)
            else:  # Puntos superiores
                puntos_mod[j][1] -= int(apertura//2)
        
        # Dibujar boca "abierta" en negro
        cv2.fillPoly(frame, [puntos_mod], (0, 0, 0))
        out.write(frame)
    
    out.release()
    return salida_avi

def combinar_audio_video(video_path, audio_path, salida_final):
    """Combinar video y audio con ffmpeg"""
    try:
        cmd = ['ffmpeg', '-y', '-i', video_path, '-i', audio_path, '-shortest', '-c:v', 'copy', '-c:a', 'aac', salida_final]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if proc.returncode == 0:
            return True, salida_final
        else:
            return False, proc.stderr
    except Exception as e:
        return False, str(e)

class AppSimple:
    def __init__(self, root):
        self.root = root
        root.title("Animación Simple - Sin MediaPipe")
        root.geometry("600x400")
        self.imagen_path = None

        frm = tk.Frame(root, padx=15, pady=15)
        frm.pack(fill=tk.BOTH, expand=True)

        # Título
        title = tk.Label(frm, text="🎭 Animación de Labios Simplificada", font=("Arial", 16, "bold"))
        title.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Selección de imagen
        tk.Label(frm, text="1) Selecciona una imagen:").grid(row=1, column=0, sticky="w", pady=(0, 10))
        btn_img = tk.Button(frm, text="📁 Seleccionar imagen", command=self.seleccionar_imagen)
        btn_img.grid(row=1, column=1, sticky="w", pady=(0, 10))

        # Texto a decir
        tk.Label(frm, text="2) Texto a decir:").grid(row=2, column=0, sticky="w", pady=(0, 10))
        self.texto_entry = tk.Entry(frm, width=50)
        self.texto_entry.grid(row=2, column=1, sticky="w", pady=(0, 10))
        self.texto_entry.insert(0, "Hola, soy un avatar animado con inteligencia artificial")

        # Nombre de salida
        tk.Label(frm, text="3) Nombre del video:").grid(row=3, column=0, sticky="w", pady=(0, 10))
        self.salida_entry = tk.Entry(frm, width=50)
        self.salida_entry.grid(row=3, column=1, sticky="w", pady=(0, 10))
        self.salida_entry.insert(0, "mi_animacion")

        # Estado
        self.status = tk.Label(frm, text="📱 Estado: Listo para comenzar", anchor="w", justify="left", fg="blue")
        self.status.grid(row=4, column=0, columnspan=2, sticky="we", pady=(20, 10))

        # Botón generar
        btn_gen = tk.Button(frm, text="🎬 Generar Animación", command=self.on_generar, 
                           bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), height=2)
        btn_gen.grid(row=5, column=0, columnspan=2, pady=(20, 10))

        # Instrucciones
        instrucciones = tk.Label(frm, text="""
📋 Instrucciones:
• Selecciona una imagen con una cara visible
• Escribe el texto que quieres que "diga"
• Click en 'Generar Animación'
• El video se guardará en la carpeta 'resultados'
        """, justify="left", anchor="w")
        instrucciones.grid(row=6, column=0, columnspan=2, sticky="we", pady=(20, 0))

    def seleccionar_imagen(self):
        path = filedialog.askopenfilename(filetypes=[("Imágenes", "*.jpg *.jpeg *.png *.bmp")])
        if path:
            self.imagen_path = path
            self.status.config(text=f"📷 Imagen seleccionada: {os.path.basename(path)}", fg="green")

    def on_generar(self):
        if not self.imagen_path:
            messagebox.showwarning("Error", "❌ Selecciona primero una imagen")
            return
        
        texto = self.texto_entry.get().strip()
        if not texto:
            messagebox.showwarning("Error", "❌ Escribe un texto para generar audio")
            return
            
        nombre = self.salida_entry.get().strip() or "animacion"
        
        # Ejecutar en hilo separado para no bloquear la UI
        threading.Thread(target=self.procesar, args=(self.imagen_path, texto, nombre), daemon=True).start()

    def procesar(self, imagen_path, texto, nombre_salida):
        try:
            self.status.config(text="⏳ Cargando imagen...", fg="orange")
            
            # Cargar imagen
            img = cv2.imread(imagen_path)
            if img is None:
                self.status.config(text="❌ Error: No se pudo cargar la imagen", fg="red")
                return

            # Crear directorio de resultados
            out_dir = "resultados"
            os.makedirs(out_dir, exist_ok=True)

            self.status.config(text="🎨 Aplicando filtro cartoon...", fg="orange")
            
            # Cartoonizar imagen
            cartoon = cartoonify_image(img)
            cartoon_path = os.path.join(out_dir, f"{nombre_salida}_cartoon.jpg")
            cv2.imwrite(cartoon_path, cartoon)

            self.status.config(text="👁️ Detectando cara...", fg="orange")
            
            # Detectar cara y labios
            puntos, coords_cara = detectar_cara_simple(cartoon)
            if puntos is None:
                self.status.config(text="❌ No se detectó cara en la imagen. Prueba otra imagen.", fg="red")
                return

            # Mostrar información de la cara detectada
            if coords_cara:
                x, y, w, h = coords_cara
                print(f"✅ Cara detectada: {w}x{h} píxeles en posición ({x}, {y})")

            self.status.config(text="🎤 Generando audio...", fg="orange")
            
            # Generar audio
            audio_path = os.path.join(out_dir, f"{nombre_salida}.wav")
            generar_voz(texto, audio_path)

            self.status.config(text="🎬 Creando animación...", fg="orange")
            
            # Animar labios
            video_path = os.path.join(out_dir, f"{nombre_salida}.avi")
            animar_labios_simple(cartoon, puntos, video_path, fps=25, frames_count=50)

            self.status.config(text="🔊 Combinando audio y video...", fg="orange")
            
            # Combinar con audio
            final_path = os.path.join(out_dir, f"{nombre_salida}_final.mp4")
            ok, msg = combinar_audio_video(video_path, audio_path, final_path)
            
            if ok:
                self.status.config(text=f"✅ ¡Listo! Video guardado: {final_path}", fg="green")
                messagebox.showinfo("✅ Éxito", f"¡Video creado exitosamente!\n\n📁 Ubicación: {final_path}")
            else:
                self.status.config(text=f"⚠️ Video creado: {video_path} (ffmpeg no disponible)", fg="orange")
                messagebox.showinfo("⚠️ Parcial", f"Video creado pero sin audio integrado:\n\n📁 Video: {video_path}\n🎵 Audio: {audio_path}")

        except Exception as e:
            self.status.config(text=f"❌ Error: {str(e)}", fg="red")
            messagebox.showerror("Error", f"❌ Error durante el procesamiento:\n{str(e)}")

if __name__ == '__main__':
    root = tk.Tk()
    app = AppSimple(root)
    root.mainloop()