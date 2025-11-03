#!/usr/bin/env python3
"""
Script de prueba automática para la interfaz ultra simple
"""
import os
import sys
import time
from PIL import Image, ImageFilter, ImageEnhance
import pyttsx3

def probar_aplicacion():
    print("🎬 PROBANDO APLICACIÓN ULTRA SIMPLE")
    print("=" * 50)
    
    # Verificar imagen de ejemplo
    imagen_ejemplo = "woman-3584435_1280.jpg"
    if not os.path.exists(imagen_ejemplo):
        print(f"❌ No se encuentra la imagen: {imagen_ejemplo}")
        return False
    
    print(f"✅ Imagen encontrada: {imagen_ejemplo}")
    
    # Crear directorio de resultados
    os.makedirs("resultados", exist_ok=True)
    print("✅ Directorio 'resultados' creado")
    
    # 1. Procesar imagen con PIL
    print("\n🎨 PROCESANDO IMAGEN...")
    try:
        img = Image.open(imagen_ejemplo)
        print(f"   📐 Tamaño original: {img.size}")
        
        # Aplicar efectos cartoon
        img = img.filter(ImageFilter.SMOOTH_MORE)
        img = img.filter(ImageFilter.EDGE_ENHANCE)
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(1.4)
        
        # Guardar imagen procesada
        imagen_procesada = os.path.join("resultados", "prueba_procesada.jpg")
        img.save(imagen_procesada, "JPEG", quality=95)
        print(f"   ✅ Imagen procesada guardada: {imagen_procesada}")
        
    except Exception as e:
        print(f"   ❌ Error procesando imagen: {e}")
        return False
    
    # 2. Generar audio
    print("\n🎤 GENERANDO AUDIO...")
    try:
        texto = "Hola, soy tu avatar virtual creado con inteligencia artificial. Esta es una prueba de la aplicación de animación ultra simple."
        audio_path = os.path.join("resultados", "prueba_audio.wav")
        
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        
        # Obtener voces disponibles
        voices = engine.getProperty('voices')
        print(f"   🎭 Voces disponibles: {len(voices)}")
        
        engine.save_to_file(texto, audio_path)
        engine.runAndWait()
        engine.stop()
        
        if os.path.exists(audio_path):
            size = os.path.getsize(audio_path)
            print(f"   ✅ Audio generado: {audio_path} ({size} bytes)")
        else:
            print(f"   ❌ No se pudo crear el audio")
            return False
            
    except Exception as e:
        print(f"   ❌ Error generando audio: {e}")
        return False
    
    # 3. Intentar crear video con ffmpeg (opcional)
    print("\n🎬 INTENTANDO CREAR VIDEO...")
    try:
        import subprocess
        video_path = os.path.join("resultados", "prueba_final.mp4")
        
        cmd = [
            'ffmpeg', '-y',
            '-loop', '1', '-i', imagen_procesada,
            '-i', audio_path,
            '-c:v', 'libx264', '-t', '5',
            '-pix_fmt', 'yuv420p', '-shortest',
            video_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0 and os.path.exists(video_path):
            size = os.path.getsize(video_path)
            print(f"   ✅ Video creado: {video_path} ({size} bytes)")
        else:
            print(f"   ⚠️ FFmpeg no disponible o falló")
            print(f"   💡 Archivos separados creados correctamente")
            
    except Exception as e:
        print(f"   ⚠️ FFmpeg no disponible: {e}")
        print(f"   💡 Los archivos de audio e imagen se crearon correctamente")
    
    # 4. Resumen de resultados
    print("\n📋 RESUMEN DE RESULTADOS:")
    resultados_dir = "resultados"
    if os.path.exists(resultados_dir):
        archivos = os.listdir(resultados_dir)
        for archivo in archivos:
            if archivo.startswith("prueba"):
                path = os.path.join(resultados_dir, archivo)
                size = os.path.getsize(path)
                print(f"   📁 {archivo} - {size} bytes")
    
    print(f"\n🎉 ¡PRUEBA COMPLETADA!")
    print(f"📂 Revisa la carpeta 'resultados' para ver los archivos generados")
    return True

if __name__ == "__main__":
    probar_aplicacion()