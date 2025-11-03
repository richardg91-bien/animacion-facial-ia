#!/usr/bin/env python3
"""
Versión ULTRA simplificada - Solo procesamiento de audio sin OpenCV
Para casos donde OpenCV no funciona por problemas de compatibilidad
"""
import os
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import pyttsx3
from PIL import Image, ImageTk, ImageFilter, ImageEnhance
import subprocess

class AnimacionUltraSimple:
    def __init__(self, root):
        self.root = root
        root.title("🎬 Animación Ultra Simple - Solo Audio + Imagen")
        root.geometry("700x500")
        root.configure(bg="#2c3e50")
        self.imagen_path = None
        self.imagen_preview = None

        # Frame principal
        main_frame = tk.Frame(root, bg="#2c3e50", padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Título
        title = tk.Label(main_frame, text="🎬 Creador de Videos Animados", 
                        font=("Arial", 20, "bold"), bg="#2c3e50", fg="#ecf0f1")
        title.pack(pady=(0, 30))

        # Frame superior para imagen y controles
        top_frame = tk.Frame(main_frame, bg="#2c3e50")
        top_frame.pack(fill="x", pady=(0, 20))

        # Panel izquierdo - Preview de imagen
        left_panel = tk.Frame(top_frame, bg="#34495e", relief="raised", bd=2)
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))

        tk.Label(left_panel, text="📷 Vista Previa", font=("Arial", 14, "bold"), 
                bg="#34495e", fg="#ecf0f1").pack(pady=10)

        self.image_label = tk.Label(left_panel, text="Selecciona una imagen\npara ver vista previa", 
                                   bg="#34495e", fg="#bdc3c7", font=("Arial", 12),
                                   width=30, height=15)
        self.image_label.pack(pady=20)

        btn_select = tk.Button(left_panel, text="📁 Seleccionar Imagen", 
                              command=self.seleccionar_imagen,
                              bg="#3498db", fg="white", font=("Arial", 12, "bold"),
                              padx=20, pady=10)
        btn_select.pack(pady=10)

        # Panel derecho - Controles
        right_panel = tk.Frame(top_frame, bg="#34495e", relief="raised", bd=2)
        right_panel.pack(side="right", fill="both", expand=True, padx=(10, 0))

        tk.Label(right_panel, text="⚙️ Configuración", font=("Arial", 14, "bold"), 
                bg="#34495e", fg="#ecf0f1").pack(pady=10)

        # Texto a decir
        tk.Label(right_panel, text="📝 Texto a convertir:", font=("Arial", 12), 
                bg="#34495e", fg="#ecf0f1").pack(anchor="w", padx=10, pady=(10, 5))
        
        self.texto_box = tk.Text(right_panel, height=6, width=40, font=("Arial", 11), wrap=tk.WORD)
        self.texto_box.pack(padx=10, pady=(0, 10), fill="x")
        self.texto_box.insert("1.0", "Hola, soy tu avatar virtual. Este texto se convertirá en audio para animar la imagen seleccionada.")

        # Nombre del proyecto
        name_frame = tk.Frame(right_panel, bg="#34495e")
        name_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(name_frame, text="📁 Nombre:", bg="#34495e", fg="#ecf0f1").pack(side="left")
        self.nombre_entry = tk.Entry(name_frame, font=("Arial", 11))
        self.nombre_entry.pack(side="right", fill="x", expand=True, padx=(10, 0))
        self.nombre_entry.insert(0, "mi_proyecto")

        # Velocidad de voz
        speed_frame = tk.Frame(right_panel, bg="#34495e")
        speed_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(speed_frame, text="⚡ Velocidad:", bg="#34495e", fg="#ecf0f1").pack(side="left")
        self.velocidad_var = tk.StringVar(value="150")
        tk.Spinbox(speed_frame, from_=50, to=300, textvariable=self.velocidad_var, width=10).pack(side="right")

        # Duración del video
        duration_frame = tk.Frame(right_panel, bg="#34495e")
        duration_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(duration_frame, text="⏱️ Duración:", bg="#34495e", fg="#ecf0f1").pack(side="left")
        self.duracion_var = tk.StringVar(value="5")
        tk.Spinbox(duration_frame, from_=3, to=30, textvariable=self.duracion_var, width=10).pack(side="right")
        tk.Label(duration_frame, text="segundos", bg="#34495e", fg="#bdc3c7").pack(side="right", padx=(0, 5))

        # Estado
        self.status_label = tk.Label(main_frame, text="📱 Listo para crear tu video animado", 
                                   font=("Arial", 12), bg="#2c3e50", fg="#27ae60")
        self.status_label.pack(pady=(20, 10))

        # Botones principales
        button_frame = tk.Frame(main_frame, bg="#2c3e50")
        button_frame.pack(pady=10)
        
        self.btn_generar = tk.Button(button_frame, text="🎬 Crear Video Animado", 
                                    command=self.crear_video,
                                    bg="#e74c3c", fg="white", font=("Arial", 14, "bold"),
                                    padx=30, pady=15)
        self.btn_generar.pack(side="left", padx=(0, 10))
        
        tk.Button(button_frame, text="🎤 Solo Audio", 
                 command=self.crear_solo_audio,
                 bg="#9b59b6", fg="white", font=("Arial", 12),
                 padx=20, pady=15).pack(side="left", padx=(10, 0))

        # Información
        info_text = tk.Label(main_frame, 
            text="💡 Esta versión crea un video simple combinando tu imagen con audio generado.\n"
                 "No requiere OpenCV ni detección facial avanzada.",
            font=("Arial", 10), bg="#2c3e50", fg="#95a5a6", justify="center")
        info_text.pack(pady=(20, 0))

    def seleccionar_imagen(self):
        path = filedialog.askopenfilename(
            title="Seleccionar Imagen",
            filetypes=[("Imágenes", "*.jpg *.jpeg *.png *.bmp *.gif")]
        )
        if path:
            self.imagen_path = path
            self.mostrar_preview(path)
            self.status_label.config(text=f"📷 Imagen cargada: {os.path.basename(path)}", fg="#27ae60")

    def mostrar_preview(self, path):
        try:
            # Cargar y redimensionar imagen para preview
            img = Image.open(path)
            img.thumbnail((250, 200), Image.Resampling.LANCZOS)
            
            # Aplicar efecto (simulando cartoon)
            img = img.filter(ImageFilter.SMOOTH_MORE)
            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance(1.3)
            
            # Convertir para tkinter
            self.imagen_preview = ImageTk.PhotoImage(img)
            self.image_label.config(image=self.imagen_preview, text="")
        except Exception as e:
            self.image_label.config(text=f"Error cargando\nimagen:\n{str(e)}")

    def crear_solo_audio(self):
        texto = self.texto_box.get("1.0", tk.END).strip()
        if not texto:
            messagebox.showwarning("Error", "❌ Escribe un texto para convertir")
            return
        
        nombre = self.nombre_entry.get().strip() or "audio"
        threading.Thread(target=self._crear_audio_thread, args=(texto, nombre), daemon=True).start()

    def crear_video(self):
        if not self.imagen_path:
            messagebox.showwarning("Error", "❌ Selecciona una imagen primero")
            return
        
        texto = self.texto_box.get("1.0", tk.END).strip()
        if not texto:
            messagebox.showwarning("Error", "❌ Escribe un texto para convertir")
            return
        
        nombre = self.nombre_entry.get().strip() or "video"
        threading.Thread(target=self._crear_video_thread, args=(texto, nombre), daemon=True).start()

    def _crear_audio_thread(self, texto, nombre):
        try:
            self.btn_generar.config(state="disabled")
            self.status_label.config(text="🎤 Generando audio...", fg="#e67e22")
            
            # Crear directorio
            os.makedirs("resultados", exist_ok=True)
            audio_path = os.path.join("resultados", f"{nombre}.wav")
            
            # Generar audio
            engine = pyttsx3.init()
            try:
                velocidad = int(self.velocidad_var.get())
                engine.setProperty('rate', velocidad)
            except:
                engine.setProperty('rate', 150)
            
            engine.save_to_file(texto, audio_path)
            engine.runAndWait()
            engine.stop()
            
            self.status_label.config(text=f"✅ Audio creado: {audio_path}", fg="#27ae60")
            messagebox.showinfo("✅ Éxito", f"¡Audio generado!\n📁 {audio_path}")
            
        except Exception as e:
            self.status_label.config(text=f"❌ Error: {str(e)}", fg="#e74c3c")
        finally:
            self.btn_generar.config(state="normal")

    def _crear_video_thread(self, texto, nombre):
        try:
            self.btn_generar.config(state="disabled")
            self.status_label.config(text="🎬 Iniciando creación de video...", fg="#e67e22")
            
            # Crear directorio
            os.makedirs("resultados", exist_ok=True)
            
            # 1. Generar audio
            self.status_label.config(text="🎤 Generando audio...", fg="#e67e22")
            audio_path = os.path.join("resultados", f"{nombre}.wav")
            
            engine = pyttsx3.init()
            try:
                velocidad = int(self.velocidad_var.get())
                engine.setProperty('rate', velocidad)
            except:
                engine.setProperty('rate', 150)
            
            engine.save_to_file(texto, audio_path)
            engine.runAndWait()
            engine.stop()
            
            # 2. Procesar imagen (aplicar efectos con PIL)
            self.status_label.config(text="🎨 Procesando imagen...", fg="#e67e22")
            img = Image.open(self.imagen_path)
            
            # Aplicar efectos cartoon con PIL
            img = img.filter(ImageFilter.SMOOTH_MORE)
            img = img.filter(ImageFilter.EDGE_ENHANCE)
            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance(1.4)
            
            # Guardar imagen procesada
            imagen_procesada = os.path.join("resultados", f"{nombre}_procesada.jpg")
            img.save(imagen_procesada, "JPEG", quality=95)
            
            # 3. Crear video con ffmpeg (si está disponible)
            self.status_label.config(text="🎬 Creando video...", fg="#e67e22")
            
            try:
                duracion = int(self.duracion_var.get())
            except:
                duracion = 5
            
            video_path = os.path.join("resultados", f"{nombre}_final.mp4")
            
            # Comando ffmpeg para crear video desde imagen estática
            cmd = [
                'ffmpeg', '-y',
                '-loop', '1', '-i', imagen_procesada,
                '-i', audio_path,
                '-c:v', 'libx264', '-t', str(duracion),
                '-pix_fmt', 'yuv420p', '-shortest',
                video_path
            ]
            
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
                if result.returncode == 0 and os.path.exists(video_path):
                    self.status_label.config(text=f"✅ ¡Video creado! {video_path}", fg="#27ae60")
                    messagebox.showinfo("🎉 ¡Éxito!", 
                        f"¡Video animado creado exitosamente!\n\n"
                        f"📁 Video: {video_path}\n"
                        f"🎵 Audio: {audio_path}\n"
                        f"🖼️ Imagen: {imagen_procesada}")
                else:
                    raise Exception("FFmpeg falló")
            except:
                # Si ffmpeg no está disponible, mostrar archivos creados
                self.status_label.config(text="⚠️ Video parcial creado (instala FFmpeg para combinar)", fg="#f39c12")
                messagebox.showinfo("⚠️ Parcial", 
                    f"Archivos creados por separado:\n\n"
                    f"🎵 Audio: {audio_path}\n"
                    f"🖼️ Imagen procesada: {imagen_procesada}\n\n"
                    f"💡 Instala FFmpeg para crear video automáticamente")
            
        except Exception as e:
            self.status_label.config(text=f"❌ Error: {str(e)}", fg="#e74c3c")
            messagebox.showerror("Error", f"❌ Error creando video:\n{str(e)}")
        finally:
            self.btn_generar.config(state="normal")

if __name__ == "__main__":
    root = tk.Tk()
    app = AnimacionUltraSimple(root)
    root.mainloop()