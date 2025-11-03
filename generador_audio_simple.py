#!/usr/bin/env python3
"""
Generador de Audio Simple
Solo convierte texto a voz - sin procesamiento de video ni imágenes
"""
import os
import tkinter as tk
from tkinter import messagebox, filedialog
import pyttsx3
import threading

class AudioGenerator:
    def __init__(self, root):
        self.root = root
        root.title("🎤 Generador de Audio - Text to Speech")
        root.geometry("500x400")
        root.configure(bg="#f0f0f0")

        # Frame principal
        main_frame = tk.Frame(root, bg="#f0f0f0", padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Título
        title = tk.Label(main_frame, text="🎤 Generador de Audio", 
                        font=("Arial", 18, "bold"), bg="#f0f0f0", fg="#2c3e50")
        title.pack(pady=(0, 20))

        # Texto a convertir
        tk.Label(main_frame, text="📝 Texto a convertir en audio:", 
                font=("Arial", 12), bg="#f0f0f0").pack(anchor="w", pady=(0, 5))
        
        self.texto_frame = tk.Frame(main_frame, bg="#f0f0f0")
        self.texto_frame.pack(fill="both", expand=True, pady=(0, 15))
        
        self.texto_box = tk.Text(self.texto_frame, height=8, width=60, 
                               font=("Arial", 11), wrap=tk.WORD)
        scrollbar = tk.Scrollbar(self.texto_frame, orient="vertical", command=self.texto_box.yview)
        self.texto_box.configure(yscrollcommand=scrollbar.set)
        
        self.texto_box.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Texto por defecto
        self.texto_box.insert("1.0", 
            "Hola, soy un avatar animado con inteligencia artificial. "
            "Este es un ejemplo de síntesis de voz que convierte texto en audio de manera natural. "
            "Puedes cambiar este texto por cualquier mensaje que quieras.")

        # Nombre del archivo
        name_frame = tk.Frame(main_frame, bg="#f0f0f0")
        name_frame.pack(fill="x", pady=(0, 15))
        
        tk.Label(name_frame, text="📁 Nombre del archivo:", 
                font=("Arial", 12), bg="#f0f0f0").pack(side="left")
        
        self.nombre_entry = tk.Entry(name_frame, font=("Arial", 11), width=25)
        self.nombre_entry.pack(side="right")
        self.nombre_entry.insert(0, "mi_audio")

        # Configuración de voz
        config_frame = tk.Frame(main_frame, bg="#f0f0f0")
        config_frame.pack(fill="x", pady=(0, 15))
        
        tk.Label(config_frame, text="⚡ Velocidad:", 
                font=("Arial", 11), bg="#f0f0f0").pack(side="left")
        
        self.velocidad_var = tk.StringVar(value="150")
        velocidad_combo = tk.Spinbox(config_frame, from_=50, to=300, 
                                   textvariable=self.velocidad_var, width=10)
        velocidad_combo.pack(side="left", padx=(5, 15))
        
        tk.Label(config_frame, text="🎭 Voz:", 
                font=("Arial", 11), bg="#f0f0f0").pack(side="left")
        
        self.voz_var = tk.StringVar()
        self.voz_combo = tk.Spinbox(config_frame, values=self.get_voices(), 
                                  textvariable=self.voz_var, width=15, state="readonly")
        self.voz_combo.pack(side="left", padx=(5, 0))

        # Estado
        self.status_label = tk.Label(main_frame, text="📱 Listo para generar audio", 
                                   font=("Arial", 10), bg="#f0f0f0", fg="#27ae60")
        self.status_label.pack(pady=(15, 10))

        # Botones
        button_frame = tk.Frame(main_frame, bg="#f0f0f0")
        button_frame.pack(pady=(0, 10))
        
        self.generate_btn = tk.Button(button_frame, text="🎵 Generar Audio", 
                                    command=self.generar_audio, 
                                    bg="#3498db", fg="white", font=("Arial", 12, "bold"),
                                    padx=20, pady=10)
        self.generate_btn.pack(side="left", padx=(0, 10))
        
        tk.Button(button_frame, text="🔊 Probar Voz", 
                 command=self.probar_voz, 
                 bg="#e74c3c", fg="white", font=("Arial", 12),
                 padx=20, pady=10).pack(side="left", padx=(10, 0))

        # Instrucciones
        instrucciones = tk.Label(main_frame, 
            text="💡 Escribe tu texto, ajusta la configuración y genera el audio.\n"
                 "Los archivos se guardan en formato WAV en la carpeta actual.",
            font=("Arial", 9), bg="#f0f0f0", fg="#7f8c8d", justify="center")
        instrucciones.pack(pady=(15, 0))

    def get_voices(self):
        """Obtener lista de voces disponibles"""
        try:
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            voice_names = []
            for i, voice in enumerate(voices[:5]):  # Máximo 5 voces
                name = voice.name if hasattr(voice, 'name') else f"Voz {i+1}"
                voice_names.append(name)
            engine.stop()
            return voice_names if voice_names else ["Voz por defecto"]
        except:
            return ["Voz por defecto"]

    def probar_voz(self):
        """Probar la voz seleccionada"""
        threading.Thread(target=self._probar_voz_thread, daemon=True).start()

    def _probar_voz_thread(self):
        try:
            self.status_label.config(text="🔊 Probando voz...", fg="#e67e22")
            engine = pyttsx3.init()
            
            # Configurar velocidad
            try:
                velocidad = int(self.velocidad_var.get())
                engine.setProperty('rate', velocidad)
            except:
                pass
            
            # Configurar voz
            try:
                voices = engine.getProperty('voices')
                voz_seleccionada = self.voz_var.get()
                for i, voice in enumerate(voices):
                    if voice.name == voz_seleccionada:
                        engine.setProperty('voice', voice.id)
                        break
            except:
                pass
            
            # Decir texto de prueba
            engine.say("Hola, esta es una prueba de voz")
            engine.runAndWait()
            engine.stop()
            
            self.status_label.config(text="✅ Prueba de voz completada", fg="#27ae60")
        except Exception as e:
            self.status_label.config(text=f"❌ Error en prueba: {str(e)}", fg="#e74c3c")

    def generar_audio(self):
        texto = self.texto_box.get("1.0", tk.END).strip()
        if not texto:
            messagebox.showwarning("Error", "❌ Escribe un texto para convertir")
            return
        
        nombre = self.nombre_entry.get().strip()
        if not nombre:
            nombre = "audio_generado"
        
        # Ejecutar en hilo separado
        threading.Thread(target=self._generar_audio_thread, 
                        args=(texto, nombre), daemon=True).start()

    def _generar_audio_thread(self, texto, nombre):
        try:
            self.generate_btn.config(state="disabled")
            self.status_label.config(text="🎤 Generando audio...", fg="#e67e22")
            
            # Crear directorio de salida
            output_dir = "audios_generados"
            os.makedirs(output_dir, exist_ok=True)
            
            # Ruta del archivo
            audio_path = os.path.join(output_dir, f"{nombre}.wav")
            
            # Configurar engine
            engine = pyttsx3.init()
            
            try:
                velocidad = int(self.velocidad_var.get())
                engine.setProperty('rate', velocidad)
            except:
                engine.setProperty('rate', 150)
            
            # Configurar voz
            try:
                voices = engine.getProperty('voices')
                voz_seleccionada = self.voz_var.get()
                for voice in voices:
                    if hasattr(voice, 'name') and voice.name == voz_seleccionada:
                        engine.setProperty('voice', voice.id)
                        break
            except:
                pass
            
            # Generar archivo
            engine.save_to_file(texto, audio_path)
            engine.runAndWait()
            engine.stop()
            
            if os.path.exists(audio_path):
                self.status_label.config(text=f"✅ Audio guardado: {audio_path}", fg="#27ae60")
                messagebox.showinfo("✅ Éxito", 
                    f"¡Audio generado exitosamente!\n\n"
                    f"📁 Archivo: {audio_path}\n"
                    f"📝 Caracteres: {len(texto)}\n"
                    f"⚡ Velocidad: {self.velocidad_var.get()} WPM")
            else:
                self.status_label.config(text="❌ Error: No se pudo crear el archivo", fg="#e74c3c")
                
        except Exception as e:
            self.status_label.config(text=f"❌ Error: {str(e)}", fg="#e74c3c")
            messagebox.showerror("Error", f"❌ Error al generar audio:\n{str(e)}")
        finally:
            self.generate_btn.config(state="normal")

if __name__ == "__main__":
    root = tk.Tk()
    app = AudioGenerator(root)
    root.mainloop()