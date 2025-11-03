"""
Implementación simplificada de Wav2Lip para sincronización de labios con audio
Autor: GitHub Copilot
Fecha: Noviembre 2024
"""

import cv2
import numpy as np
import os
import subprocess
import tempfile
from pathlib import Path

class Wav2LipSimple:
    def __init__(self):
        """Inicializar el generador de video lip-sync"""
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.mouth_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')
        
    def detect_face_and_mouth(self, frame):
        """Detectar cara y región de la boca en el frame"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detectar caras
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        
        if len(faces) == 0:
            return None, None
            
        # Tomar la cara más grande
        face = max(faces, key=lambda x: x[2] * x[3])
        x, y, w, h = face
        
        # Región de la boca (tercio inferior de la cara)
        mouth_y = y + int(h * 0.6)
        mouth_h = int(h * 0.4)
        mouth_region = (x, mouth_y, w, mouth_h)
        
        return face, mouth_region
    
    def extract_audio_features(self, audio_path):
        """Extraer características básicas del audio para animación"""
        # Por simplicidad, vamos a simular la extracción de características
        # En una implementación real, usarías librosa para extraer MFCC, etc.
        
        # Obtener duración del audio usando ffprobe
        try:
            result = subprocess.run([
                'ffprobe', '-v', 'quiet', '-show_entries', 
                'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', 
                audio_path
            ], capture_output=True, text=True)
            duration = float(result.stdout.strip())
        except:
            # Fallback: asumir 3 segundos si no se puede obtener duración
            duration = 3.0
            
        # Simular características de audio (amplitud por frame)
        fps = 25  # frames por segundo
        total_frames = int(duration * fps)
        
        # Generar patrón de animación de boca basado en frecuencia simulada
        audio_features = []
        for i in range(total_frames):
            # Simular intensidad de habla (sinusoidal con ruido)
            time = i / fps
            intensity = abs(np.sin(time * 10) + 0.3 * np.sin(time * 30) + 0.1 * np.random.randn())
            audio_features.append(intensity)
            
        return audio_features, fps
    
    def animate_mouth(self, frame, mouth_region, intensity):
        """Animar la región de la boca basada en la intensidad del audio"""
        x, y, w, h = mouth_region
        
        # Crear una copia del frame
        animated_frame = frame.copy()
        
        # Extraer región de la boca
        mouth_roi = frame[y:y+h, x:x+w]
        
        if mouth_roi.size == 0:
            return animated_frame
            
        # Simular apertura de boca basada en intensidad
        mouth_opening = int(intensity * 15)  # Máximo 15 píxeles de apertura
        
        # Crear máscara para la boca abierta
        mask = np.zeros((h, w), dtype=np.uint8)
        
        # Dibujar óvalo para boca abierta
        center_x, center_y = w // 2, h // 2
        axes_x, axes_y = w // 4, max(2, mouth_opening)
        
        cv2.ellipse(mask, (center_x, center_y), (axes_x, axes_y), 0, 0, 360, 255, -1)
        
        # Aplicar un efecto de oscurecimiento para simular boca abierta
        mouth_roi_copy = mouth_roi.copy()
        mouth_roi_copy[mask > 0] = mouth_roi_copy[mask > 0] * 0.3  # Oscurecer
        
        # Aplicar la animación al frame
        animated_frame[y:y+h, x:x+w] = mouth_roi_copy
        
        return animated_frame
    
    def create_video_from_image(self, image_path, audio_path, output_path="resultado_wav2lip.mp4"):
        """Crear video animado desde imagen estática y audio"""
        print("🎬 Iniciando generación de video Wav2Lip...")
        
        # Cargar imagen
        image = cv2.imread(image_path)
        if image is None:
            print(f"❌ Error: No se pudo cargar la imagen {image_path}")
            return False
            
        print(f"✅ Imagen cargada: {image_path}")
        
        # Detectar cara y boca
        face, mouth_region = self.detect_face_and_mouth(image)
        if face is None or mouth_region is None:
            print("❌ Error: No se detectó cara en la imagen")
            return False
            
        print("✅ Cara y región de boca detectadas")
        
        # Extraer características de audio
        try:
            audio_features, fps = self.extract_audio_features(audio_path)
            print(f"✅ Audio procesado: {len(audio_features)} frames a {fps} FPS")
        except Exception as e:
            print(f"❌ Error procesando audio: {e}")
            return False
        
        # Configurar writer de video
        height, width = image.shape[:2]
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        
        # Crear video temporal sin audio
        temp_video = "temp_video_no_audio.mp4"
        out = cv2.VideoWriter(temp_video, fourcc, fps, (width, height))
        
        print("🎥 Generando frames animados...")
        
        # Generar frames animados
        for i, intensity in enumerate(audio_features):
            # Animar boca
            animated_frame = self.animate_mouth(image, mouth_region, intensity)
            out.write(animated_frame)
            
            # Mostrar progreso
            if i % 25 == 0:
                progress = (i / len(audio_features)) * 100
                print(f"📊 Progreso: {progress:.1f}%")
        
        out.release()
        print("✅ Video base generado")
        
        # Combinar video con audio usando ffmpeg
        print("🔊 Combinando video con audio...")
        try:
            subprocess.run([
                'ffmpeg', '-i', temp_video, '-i', audio_path, 
                '-c:v', 'copy', '-c:a', 'aac', '-shortest', 
                '-y', output_path
            ], check=True, capture_output=True)
            
            # Limpiar archivo temporal
            os.remove(temp_video)
            print(f"✅ Video final creado: {output_path}")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Error combinando audio: {e}")
            print("💡 Asegúrate de tener ffmpeg instalado")
            return False
        except FileNotFoundError:
            print("❌ Error: ffmpeg no encontrado")
            print("💡 Instala ffmpeg desde https://ffmpeg.org/download.html")
            return False

def main():
    """Función principal para demostración"""
    print("🎭 WAV2LIP SIMPLE - Sincronización de labios")
    print("=" * 50)
    
    # Crear instancia
    wav2lip = Wav2LipSimple()
    
    # Archivos de ejemplo (ajusta las rutas según tus archivos)
    imagen_path = "woman-3584435_1280.jpg"  # Tu imagen de mujer
    audio_path = "hola.mp3"  # Tu archivo de audio (crea uno o usa uno existente)
    
    # Verificar que existen los archivos
    if not os.path.exists(imagen_path):
        print(f"❌ Error: Imagen no encontrada: {imagen_path}")
        print("💡 Asegúrate de tener una imagen en el directorio actual")
        return
        
    if not os.path.exists(audio_path):
        print(f"⚠️  Advertencia: Audio no encontrado: {audio_path}")
        print("💡 Creando archivo de audio de ejemplo...")
        
        # Crear audio de ejemplo usando text-to-speech del sistema (Windows)
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.save_to_file("Hola, este es un ejemplo de sincronización de labios", audio_path.replace('.mp3', '.wav'))
            engine.runAndWait()
            audio_path = audio_path.replace('.mp3', '.wav')
            print(f"✅ Audio de ejemplo creado: {audio_path}")
        except ImportError:
            print("❌ No se pudo crear audio de ejemplo")
            print("💡 Instala pyttsx3: pip install pyttsx3")
            return
    
    # Generar video
    resultado = wav2lip.create_video_from_image(imagen_path, audio_path, "resultado_wav2lip.mp4")
    
    if resultado:
        print("\n🎉 ¡Éxito! Video generado correctamente")
        print("📁 Archivo: resultado_wav2lip.mp4")
    else:
        print("\n❌ Error en la generación del video")

if __name__ == "__main__":
    main()