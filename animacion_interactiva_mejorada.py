#!/usr/bin/env python3
"""
animacion_interactiva_mejorada.py
Versión mejorada con:
1) Llamada adaptativa a wav2lip_mejorado (import y uso directo si está disponible).
2) Fallback de animación de labios con blending y suavizado.
3) Interfaz GUI con opción de procesar toda una carpeta en lote.
4) Controles de voz (velocidad y selección de voz).
5) Permite modo script para ejecutar una prueba automática.
"""
import os, sys, threading, subprocess, shutil
import cv2, numpy as np, pyttsx3
import mediapipe as mp
import tkinter as tk
from tkinter import filedialog, messagebox

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXTRAS_DIR = os.path.join(BASE_DIR, "extras")
RESULTS_DIR = os.path.join(BASE_DIR, "resultados")
os.makedirs(RESULTS_DIR, exist_ok=True)

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

def generar_voz(texto, salida_mp3, rate=150, voice_index=None):
    engine = pyttsx3.init()
    try:
        engine.setProperty('rate', rate)
    except Exception:
        pass
    if voice_index is not None:
        try:
            voices = engine.getProperty('voices')
            if 0 <= voice_index < len(voices):
                engine.setProperty('voice', voices[voice_index].id)
        except Exception:
            pass
    engine.save_to_file(texto, salida_mp3)
    engine.runAndWait()
    return salida_mp3

def detectar_labios_mediapipe(imagen):
    with mp_face_mesh.FaceMesh(static_image_mode=True, refine_landmarks=True) as face_mesh:
        img_rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
        res = face_mesh.process(img_rgb)
        if not res.multi_face_landmarks:
            return None
        lm = res.multi_face_landmarks[0]
        h, w, _ = imagen.shape
        indices = list(range(61, 88))
        puntos = []
        for idx in indices:
            l = lm.landmark[idx]
            puntos.append((int(l.x * w), int(l.y * h)))
        return np.array(puntos, np.int32)

def animar_labios_blend(imagen, puntos_labios, salida_avi, fps=25, frames_count=40):
    """
    Genera animación de labios pero en lugar de pintar negro, crea una máscara
    y modifica la región de la boca con un ligero oscurecimiento y blending,
    luego aplica suavizado para naturalizar.
    """
    h, w, _ = imagen.shape
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(salida_avi, fourcc, fps, (w, h))
    mask_base = np.zeros((h, w), np.uint8)
    cv2.fillPoly(mask_base, [puntos_labios], 255)
    # Extraer bounding box de labios para operaciones localizadas
    x,y,wbox,hbox = cv2.boundingRect(puntos_labios)
    for i in range(frames_count):
        frame = imagen.copy().astype(np.float32)/255.0
        apertura = abs((i % (frames_count//2)) - (frames_count//4)) / max(1,(frames_count//4))
        # crear desplazamiento vertical para los puntos inferiores
        pts_mod = puntos_labios.copy()
        for j in range(len(pts_mod)):
            if j > len(pts_mod)//2:
                pts_mod[j][1] += int(apertura * 8)
            else:
                pts_mod[j][1] -= int(apertura * 3)
        # crear máscara animada
        mask = np.zeros((h,w), np.uint8)
        cv2.fillPoly(mask,[pts_mod],255)
        mask3 = np.stack([mask/255.0]*3, axis=-1)
        # oscurecer ligeramente la región labial para simular apertura y sombra
        region = frame * 0.9
        blended = frame*(1-mask3) + region*mask3
        # suavizado local para evitar bordes duros
        roi = (max(0,y-10), max(0,x-10), min(h,hbox+20), min(w,wbox+20))
        # apply gaussian blur on whole for simplicity
        out_frame = (cv2.GaussianBlur((blended*255).astype(np.uint8),(7,7),0))
        out.write(out_frame)
    out.release()
    return salida_avi

def try_import_wav2lip():
    """
    Intenta importar la clase Wav2LipMejorado desde extras/wav2lip_mejorado.py
    y devuelve una instancia si es posible.
    """
    try:
        sys.path.insert(0, EXTRAS_DIR)
        import wav2lip_mejorado as w2l
        if hasattr(w2l, "Wav2LipMejorado"):
            inst = w2l.Wav2LipMejorado()
            return inst
    except Exception as e:
        print("No se pudo importar wav2lip_mejorado:", e)
    finally:
        if EXTRAS_DIR in sys.path:
            sys.path.remove(EXTRAS_DIR)
    return None

def combinar_audio_video_ffmpeg(video_path, audio_path, salida_final):
    ffmpeg = shutil.which("ffmpeg") or "ffmpeg"
    if shutil.which("ffmpeg") is None:
        print("ffmpeg no encontrado en PATH.")
        return False, "ffmpeg not found"
    cmd = [ffmpeg, "-y", "-i", video_path, "-i", audio_path, "-shortest", "-c:v", "copy", "-c:a", "aac", salida_final]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if proc.returncode == 0:
            return True, salida_final
        else:
            return False, proc.stderr + proc.stdout
    except Exception as e:
        return False, str(e)

# --- Procesamiento por imagen (usa wav2lip si está disponible) ---
def procesar_imagen_pipeline(imagen_path, texto, nombre_salida, voice_rate=150, voice_idx=None, use_wav2lip=True):
    print("Procesando:", imagen_path)
    img = cv2.imread(imagen_path)
    if img is None:
        return False, "No se pudo leer la imagen"
    cartoon = cartoonify_image(img)
    cartoon_path = os.path.join(RESULTS_DIR, f"{nombre_salida}_cartoon.jpg")
    cv2.imwrite(cartoon_path, cartoon)
    puntos = detectar_labios_mediapipe(cartoon)
    audio_path = os.path.join(RESULTS_DIR, f"{nombre_salida}.mp3")
    generar_voz(texto, audio_path, rate=voice_rate, voice_index=voice_idx)
    final_output = os.path.join(RESULTS_DIR, f"{nombre_salida}_final.mp4")
    wav2lip_inst = None
    if use_wav2lip:
        wav2lip_inst = try_import_wav2lip()
    if wav2lip_inst is not None:
        try:
            print("Usando Wav2LipMejorado...")
            success = wav2lip_inst.create_video_from_image_advanced(imagen_path, audio_path, final_output)
            if success:
                return True, final_output
            else:
                print("Wav2Lip no produjo resultado, fallback al método interno.")
        except Exception as e:
            print("Error usando Wav2LipMejorado:", e)
    # Fallback: animación interna
    if puntos is None:
        return False, "No se detectaron labios en la imagen"
    avi_path = os.path.join(RESULTS_DIR, f"{nombre_salida}.avi")
    animar_labios_blend(cartoon, puntos, avi_path)
    ok, msg = combinar_audio_video_ffmpeg(avi_path, audio_path, final_output)
    if ok:
        return True, final_output
    else:
        # si ffmpeg falla, devolver avi y mp3
        return True, f"{avi_path} (audio separado: {audio_path})"

# ---------------- GUI ----------------
class App:
    def __init__(self, root):
        self.root = root
        root.title("Animación Interactiva Mejorada")
        root.geometry("620x360")
        self.selected_image = None
        frm = tk.Frame(root, padx=12, pady=12)
        frm.pack(fill=tk.BOTH, expand=True)

        tk.Label(frm, text="1) Selecciona imagen (o carpeta para lote)").grid(row=0, column=0, sticky="w")
        tk.Button(frm, text="Seleccionar imagen", command=self.select_image).grid(row=0, column=1, sticky="w")
        tk.Button(frm, text="Seleccionar carpeta (lote)", command=self.select_folder).grid(row=0, column=2, sticky="w")

        tk.Label(frm, text="2) Texto a decir:").grid(row=1, column=0, sticky="w", pady=(10,0))
        self.text_entry = tk.Entry(frm, width=45); self.text_entry.grid(row=1, column=1, columnspan=2, sticky="w", pady=(10,0))
        self.text_entry.insert(0, "Hola, soy...")

        tk.Label(frm, text="3) Nombre de salida:").grid(row=2, column=0, sticky="w", pady=(10,0))
        self.name_entry = tk.Entry(frm, width=45); self.name_entry.grid(row=2, column=1, columnspan=2, sticky="w", pady=(10,0))
        self.name_entry.insert(0, "salida")

        tk.Label(frm, text="Voz - velocidad (rate):").grid(row=3, column=0, sticky="w", pady=(10,0))
        self.rate_entry = tk.Entry(frm, width=10); self.rate_entry.grid(row=3, column=1, sticky="w", pady=(10,0))
        self.rate_entry.insert(0, "150")

        tk.Label(frm, text="Voz - índice de voz (opcional):").grid(row=4, column=0, sticky="w", pady=(6,0))
        self.voice_idx_entry = tk.Entry(frm, width=10); self.voice_idx_entry.grid(row=4, column=1, sticky="w", pady=(6,0))
        self.voice_idx_entry.insert(0, "")

        self.wav2lip_var = tk.IntVar(value=1)
        tk.Checkbutton(frm, text="Intentar usar Wav2LipMejorado (si está en extras/)", variable=self.wav2lip_var).grid(row=5, column=0, columnspan=3, sticky="w", pady=(10,0))

        self.status = tk.Label(frm, text="Estado: listo", anchor="w", justify="left")
        self.status.grid(row=6, column=0, columnspan=3, sticky="we", pady=(10,0))

        tk.Button(frm, text="Generar (imagen seleccionada)", command=self.on_generate).grid(row=7, column=0, pady=(12,0))
        tk.Button(frm, text="Generar lote (carpeta seleccionada)", command=self.on_generate_folder).grid(row=7, column=1, pady=(12,0))

    def select_image(self):
        p = filedialog.askopenfilename(filetypes=[("Images","*.jpg *.jpeg *.png")])
        if p:
            self.selected_image = p
            self.status.config(text=f"Imagen seleccionada: {os.path.basename(p)}")

    def select_folder(self):
        p = filedialog.askdirectory()
        if p:
            self.selected_image = p
            self.status.config(text=f"Carpeta seleccionada: {p}")

    def on_generate(self):
        if not self.selected_image or not os.path.isfile(self.selected_image):
            messagebox.showwarning("Selecciona una imagen primero")
            return
        texto = self.text_entry.get().strip()
        nombre = self.name_entry.get().strip() or os.path.splitext(os.path.basename(self.selected_image))[0]
        rate = int(self.rate_entry.get().strip() or "150")
        voice_idx = None
        try:
            v = self.voice_idx_entry.get().strip()
            if v != "": voice_idx = int(v)
        except:
            voice_idx = None
        threading.Thread(target=self._run_one, args=(self.selected_image, texto, nombre, rate, voice_idx), daemon=True).start()

    def on_generate_folder(self):
        if not self.selected_image or not os.path.isdir(self.selected_image):
            messagebox.showwarning("Selecciona una carpeta primero")
            return
        texto = self.text_entry.get().strip()
        rate = int(self.rate_entry.get().strip() or "150")
        voice_idx = None
        try:
            v = self.voice_idx_entry.get().strip()
            if v != "": voice_idx = int(v)
        except:
            voice_idx = None
        files = [os.path.join(self.selected_image,f) for f in os.listdir(self.selected_image) if f.lower().endswith(('.jpg','.jpeg','.png'))]
        threading.Thread(target=self._run_batch, args=(files, texto, rate, voice_idx), daemon=True).start()

    def _run_one(self, image_path, texto, nombre, rate, voice_idx):
        self.status.config(text="Estado: procesando...")
        ok, out = procesar_imagen_pipeline(image_path, texto, nombre, voice_rate=rate, voice_idx=voice_idx, use_wav2lip=bool(self.wav2lip_var.get()))
        self.status.config(text=f"Estado: terminado -> {out}" if ok else f"Error: {out}")
        messagebox.showinfo("Terminado", f"Resultado: {out}")

    def _run_batch(self, file_list, texto, rate, voice_idx):
        total = len(file_list)
        for i, f in enumerate(file_list,1):
            name = os.path.splitext(os.path.basename(f))[0]
            self.status.config(text=f"Procesando ({i}/{total}): {name}")
            ok, out = procesar_imagen_pipeline(f, texto.replace("{name}", name), name, voice_rate=rate, voice_idx=voice_idx, use_wav2lip=bool(self.wav2lip_var.get()))
            print("Resultado:", ok, out)
        self.status.config(text="Lote completado")
        messagebox.showinfo("Lote", f"Lote completado. Resultados en: {RESULTS_DIR}")

if __name__ == "__main__":
    # Si se pasa --test en la línea de comandos, ejecutar prueba automática con la imagen incluida
    if "--test" in sys.argv:
        sample = os.path.join(BASE_DIR, "woman-3584435_1280.jpg")
        if os.path.exists(sample):
            ok, out = procesar_imagen_pipeline(sample, "Hola, soy Ana", "prueba_ana", voice_rate=140, voice_idx=None, use_wav2lip=True)
            print("Test result:", ok, out)
            print("Archivos en resultados:", os.listdir(RESULTS_DIR))
        else:
            print("Imagen de prueba no encontrada:", sample)
        sys.exit(0)
    root = tk.Tk()
    app = App(root)
    root.mainloop()
