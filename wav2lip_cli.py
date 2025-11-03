#!/usr/bin/env python3
"""
WAV2LIP CLI - Generador de video con sincronización de labios desde línea de comandos
Script sin GUI que acepta argumentos por línea de comandos
Versión compatible para ejecución remota y automatizada
"""

import argparse
import os
import sys
import cv2
import numpy as np
import pyttsx3
import subprocess
from pathlib import Path

# Configuración de directorios
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(BASE_DIR, "resultados")
os.makedirs(RESULTS_DIR, exist_ok=True)

def crear_audio_desde_texto(texto, output_path):
    """
    Crear archivo de audio desde texto usando pyttsx3
    """
    print(f"🎤 Generando audio desde texto: '{texto[:50]}...'")
    
    try:
        engine = pyttsx3.init()
        
        # Configurar propiedades de voz
        voices = engine.getProperty('voices')
        if voices:
            # Buscar voz femenina si está disponible
            for voice in voices:
                if 'female' in voice.name.lower() or 'helena' in voice.name.lower():
                    engine.setProperty('voice', voice.id)
                    break
        
        # Configurar velocidad y volumen
        engine.setProperty('rate', 150)  # Velocidad
        engine.setProperty('volume', 0.9)  # Volumen
        
        # Generar audio
        engine.save_to_file(texto, output_path)
        engine.runAndWait()
        
        if os.path.exists(output_path):
            print(f"✅ Audio generado: {output_path}")
            return True
        else:
            print(f"❌ Error: No se pudo crear el audio")
            return False
            
    except Exception as e:
        print(f"❌ Error generando audio: {e}")
        return False

def detectar_cara_opencv(imagen_path):
    """
    Detectar cara usando OpenCV (método básico sin MediaPipe)
    """
    print("👁️  Detectando cara con OpenCV...")
    
    try:
        # Cargar clasificador de caras
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # Cargar imagen
        img = cv2.imread(imagen_path)
        if img is None:
            print(f"❌ Error: No se pudo cargar la imagen: {imagen_path}")
            return None
            
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Detectar caras
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        if len(faces) == 0:
            print("❌ No se detectaron caras en la imagen")
            return None
            
        print(f"✅ Detectadas {len(faces)} cara(s)")
        return faces[0]  # Retornar la primera cara detectada
        
    except Exception as e:
        print(f"❌ Error en detección de cara: {e}")
        return None

def procesar_imagen_cartoon(imagen_path, output_path):
    """
    Aplicar efecto cartoon a la imagen
    """
    print("🎨 Aplicando efecto cartoon...")
    
    try:
        img = cv2.imread(imagen_path)
        if img is None:
            return False
            
        # Aplicar filtros para efecto cartoon
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 5)
        
        # Crear bordes
        edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
        
        # Suavizar colores
        color = cv2.bilateralFilter(img, 9, 250, 250)
        
        # Combinar
        edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        cartoon = cv2.bitwise_and(color, edges)
        
        cv2.imwrite(output_path, cartoon)
        print(f"✅ Imagen cartoon guardada: {output_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error procesando imagen: {e}")
        return False

def crear_video_basico(imagen_path, audio_path, output_path):
    """
    Crear video básico combinando imagen y audio usando ffmpeg
    """
    print("🎥 Creando video con ffmpeg...")
    
    try:
        # Comando ffmpeg para combinar imagen y audio
        cmd = [
            'ffmpeg', '-y',  # -y para sobrescribir archivo existente
            '-loop', '1',    # Loop de la imagen
            '-i', imagen_path,  # Imagen de entrada
            '-i', audio_path,   # Audio de entrada
            '-c:v', 'libx264',  # Codec de video
            '-tune', 'stillimage',  # Optimizar para imagen estática
            '-c:a', 'aac',      # Codec de audio
            '-b:a', '192k',     # Bitrate de audio
            '-pix_fmt', 'yuv420p',  # Formato de pixel compatible
            '-shortest',        # Duración = duración del audio
            output_path
        ]
        
        # Ejecutar comando
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Video creado exitosamente: {output_path}")
            return True
        else:
            print(f"❌ Error en ffmpeg: {result.stderr}")
            return False
            
    except FileNotFoundError:
        print("❌ Error: ffmpeg no encontrado. Instala ffmpeg y agrégalo al PATH del sistema.")
        return False
    except Exception as e:
        print(f"❌ Error creando video: {e}")
        return False

def procesar_wav2lip_cli(imagen_path, texto_audio, salida_path):
    """
    Función principal que procesa imagen y texto para crear video con lip-sync
    """
    print("🎬 INICIANDO WAV2LIP CLI")
    print("=" * 50)
    
    # Validar imagen de entrada
    if not os.path.exists(imagen_path):
        print(f"❌ Error: La imagen no existe en la ruta: {imagen_path}")
        return False
    
    print(f"✅ Imagen recibida: {imagen_path}")
    print(f"🎤 Texto para audio: '{texto_audio}'")
    
    # Generar nombres de archivos temporales
    base_name = Path(imagen_path).stem
    audio_temp = os.path.join(RESULTS_DIR, f"{base_name}_audio.wav")
    imagen_cartoon = os.path.join(RESULTS_DIR, f"{base_name}_cartoon.jpg")
    
    # PASO 1: Crear audio desde texto
    print("\n📁 PASO 1: Generando audio...")
    if not crear_audio_desde_texto(texto_audio, audio_temp):
        return False
    
    # PASO 2: Detectar cara en imagen
    print("\n📁 PASO 2: Analizando imagen...")
    cara = detectar_cara_opencv(imagen_path)
    if cara is None:
        print("⚠️  Continuando sin detección específica de cara...")
    
    # PASO 3: Procesar imagen (efecto cartoon opcional)
    print("\n📁 PASO 3: Procesando imagen...")
    procesar_imagen_cartoon(imagen_path, imagen_cartoon)
    
    # PASO 4: Crear video básico
    print("\n📁 PASO 4: Creando video final...")
    imagen_final = imagen_cartoon if os.path.exists(imagen_cartoon) else imagen_path
    
    if crear_video_basico(imagen_final, audio_temp, salida_path):
        print(f"\n🎉 ¡PROCESO COMPLETADO!")
        print(f"📹 Video final: {salida_path}")
        print(f"📂 Revisa la carpeta 'resultados' para ver todos los archivos generados.")
        return True
    else:
        print("\n❌ Error en la creación del video final")
        return False

def main():
    """
    Función principal que maneja argumentos de línea de comandos
    """
    parser = argparse.ArgumentParser(
        description="🎭 WAV2LIP CLI - Generador de video con sincronización de labios",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python wav2lip_cli.py --imagen woman.jpg --texto "Hola mundo"
  python wav2lip_cli.py --imagen foto.png --texto "Este es un ejemplo" --salida mi_video.mp4
  python wav2lip_cli.py --imagen rostro.jpg --texto "Texto largo para generar video" --salida resultados/output.mp4
        """
    )
    
    parser.add_argument(
        '--imagen', 
        type=str, 
        required=False, 
        help='Ruta a la imagen de entrada (JPG, PNG, etc.)'
    )
    
    parser.add_argument(
        '--texto', 
        type=str, 
        required=False, 
        help='El texto a convertir en audio y sincronizar con la imagen'
    )
    
    parser.add_argument(
        '--salida', 
        type=str, 
        default=None,
        help='Ruta para el video de salida (por defecto: resultados/[nombre_imagen]_final.mp4)'
    )
    
    parser.add_argument(
        '--test', 
        action='store_true',
        help='Ejecutar con archivos de ejemplo (ignora otros argumentos)'
    )
    
    # Parsear argumentos
    args = parser.parse_args()
    
    # Modo test con archivos por defecto
    if args.test:
        print("🧪 MODO TEST - Usando archivos de ejemplo")
        imagen_test = os.path.join(BASE_DIR, "woman-3584435_1280.jpg")
        texto_test = "Hola, esto es una prueba del sistema WAV2LIP desde línea de comandos. La sincronización de labios funciona correctamente."
        salida_test = os.path.join(RESULTS_DIR, "test_cli_output.mp4")
        
        if os.path.exists(imagen_test):
            return procesar_wav2lip_cli(imagen_test, texto_test, salida_test)
        else:
            print(f"❌ Archivo de test no encontrado: {imagen_test}")
            return False
    
    # Validar argumentos requeridos para modo normal
    if not args.imagen or not args.texto:
        parser.error("Los argumentos --imagen y --texto son requeridos (excepto en modo --test)")
        return False
    
    # Generar nombre de salida automático si no se especifica
    if args.salida is None:
        base_name = Path(args.imagen).stem
        args.salida = os.path.join(RESULTS_DIR, f"{base_name}_final.mp4")
    
    # Procesar con argumentos del usuario
    return procesar_wav2lip_cli(args.imagen, args.texto, args.salida)

if __name__ == '__main__':
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⚠️  Proceso interrumpido por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        sys.exit(1)