"""
WAV2LIP SUITE - Sistema completo de sincronización de labios
Incluye múltiples implementaciones: Simple, Mejorado y Original
"""

import os
import sys
from pathlib import Path

def mostrar_menu():
    """Mostrar menú de opciones"""
    print("🎭 WAV2LIP SUITE - Sincronización de Labios")
    print("=" * 50)
    print("Selecciona una opción:")
    print()
    print("1. 🚀 Wav2Lip Simple (Rápido, funciona siempre)")
    print("2. 🎨 Wav2Lip Mejorado (Mejor calidad, usa PyTorch)")
    print("3. 🔥 Wav2Lip Original (Máxima calidad, requiere modelo)")
    print("4. 🎤 Crear nuevo audio de ejemplo")
    print("5. 📁 Ver archivos disponibles")
    print("6. ❌ Salir")
    print()

def listar_archivos():
    """Listar archivos disponibles"""
    print("\n📁 ARCHIVOS DISPONIBLES:")
    print("-" * 30)
    
    # Imágenes
    print("🖼️  IMÁGENES:")
    for ext in [".jpg", ".jpeg", ".png", ".bmp"]:
        for archivo in Path(".").glob(f"*{ext}"):
            print(f"   • {archivo.name}")
    
    # Audio
    print("\n🎵 AUDIO:")
    for ext in [".wav", ".mp3", ".m4a", ".aac"]:
        for archivo in Path(".").glob(f"*{ext}"):
            print(f"   • {archivo.name}")
    
    # Videos
    print("\n🎬 VIDEOS GENERADOS:")
    for ext in [".mp4", ".avi", ".mov"]:
        for archivo in Path(".").glob(f"*{ext}"):
            print(f"   • {archivo.name}")
    print()

def crear_audio_personalizado():
    """Crear audio personalizado"""
    try:
        import pyttsx3
        
        print("\n🎤 CREAR AUDIO PERSONALIZADO")
        print("-" * 30)
        
        texto = input("Ingresa el texto a convertir en audio: ")
        if not texto.strip():
            print("❌ Texto vacío")
            return
        
        nombre_archivo = input("Nombre del archivo (sin extensión): ")
        if not nombre_archivo.strip():
            nombre_archivo = "audio_personalizado"
        
        nombre_archivo += ".wav"
        
        # Crear audio
        engine = pyttsx3.init()
        
        # Configurar voz
        voices = engine.getProperty('voices')
        if len(voices) > 1:
            print("\n🎭 Voces disponibles:")
            for i, voice in enumerate(voices[:3]):  # Mostrar máximo 3
                print(f"{i+1}. {voice.name}")
            
            try:
                seleccion = int(input("Selecciona voz (1-3): ")) - 1
                if 0 <= seleccion < len(voices):
                    engine.setProperty('voice', voices[seleccion].id)
            except:
                print("Usando voz por defecto")
        
        # Configurar velocidad
        try:
            velocidad = int(input("Velocidad (100-200, defecto 150): "))
            if 100 <= velocidad <= 200:
                engine.setProperty('rate', velocidad)
        except:
            engine.setProperty('rate', 150)
        
        # Generar audio
        print(f"🎵 Generando audio: {nombre_archivo}")
        engine.save_to_file(texto, nombre_archivo)
        engine.runAndWait()
        
        if os.path.exists(nombre_archivo):
            print(f"✅ Audio creado: {nombre_archivo}")
        else:
            print("❌ Error creando audio")
            
    except ImportError:
        print("❌ pyttsx3 no disponible")

def ejecutar_wav2lip_simple():
    """Ejecutar versión simple"""
    print("\n🚀 EJECUTANDO WAV2LIP SIMPLE")
    print("-" * 35)
    
    # Pedir archivos
    imagen = input("Imagen (ej: woman-3584435_1280.jpg): ").strip()
    if not imagen:
        imagen = "woman-3584435_1280.jpg"
    
    audio = input("Audio (ej: hola_ejemplo.wav): ").strip()
    if not audio:
        audio = "hola_ejemplo.wav"
    
    salida = input("Video salida (ej: resultado.mp4): ").strip()
    if not salida:
        salida = "resultado_simple.mp4"
    
    # Verificar archivos
    if not os.path.exists(imagen):
        print(f"❌ Imagen no encontrada: {imagen}")
        return
    
    if not os.path.exists(audio):
        print(f"❌ Audio no encontrado: {audio}")
        return
    
    # Ejecutar
    try:
        from wav2lip_simple import Wav2LipSimple
        
        wav2lip = Wav2LipSimple()
        resultado = wav2lip.create_video_from_image(imagen, audio, salida)
        
        if resultado:
            print(f"\n✅ Video generado: {salida}")
        else:
            print("\n❌ Error en generación")
            
    except ImportError as e:
        print(f"❌ Error importando: {e}")

def ejecutar_wav2lip_mejorado():
    """Ejecutar versión mejorada"""
    print("\n🎨 EJECUTANDO WAV2LIP MEJORADO")
    print("-" * 37)
    
    # Pedir archivos
    imagen = input("Imagen (ej: woman-3584435_1280.jpg): ").strip()
    if not imagen:
        imagen = "woman-3584435_1280.jpg"
    
    audio = input("Audio (ej: hola_ejemplo.wav): ").strip()
    if not audio:
        audio = "hola_ejemplo.wav"
    
    salida = input("Video salida (ej: resultado.mp4): ").strip()
    if not salida:
        salida = "resultado_mejorado.mp4"
    
    # Verificar archivos
    if not os.path.exists(imagen):
        print(f"❌ Imagen no encontrada: {imagen}")
        return
    
    if not os.path.exists(audio):
        print(f"❌ Audio no encontrado: {audio}")
        return
    
    # Ejecutar
    try:
        from wav2lip_mejorado import Wav2LipMejorado
        
        wav2lip = Wav2LipMejorado()
        resultado = wav2lip.create_video_from_image_advanced(imagen, audio, salida)
        
        if resultado:
            print(f"\n✅ Video generado: {salida}")
        else:
            print("\n❌ Error en generación")
            
    except ImportError as e:
        print(f"❌ Error importando: {e}")

def ejecutar_wav2lip_original():
    """Ejecutar versión original"""
    print("\n🔥 EJECUTANDO WAV2LIP ORIGINAL")
    print("-" * 37)
    
    # Pedir archivos
    imagen = input("Imagen (ej: woman-3584435_1280.jpg): ").strip()
    if not imagen:
        imagen = "woman-3584435_1280.jpg"
    
    audio = input("Audio (ej: hola_ejemplo.wav): ").strip()
    if not audio:
        audio = "hola_ejemplo.wav"
    
    salida = input("Video salida (ej: resultado.mp4): ").strip()
    if not salida:
        salida = "resultado_original.mp4"
    
    # Verificar archivos
    if not os.path.exists(imagen):
        print(f"❌ Imagen no encontrada: {imagen}")
        return
    
    if not os.path.exists(audio):
        print(f"❌ Audio no encontrado: {audio}")
        return
    
    # Ejecutar
    try:
        from wav2lip_original_wrapper import run_wav2lip_original
        
        resultado = run_wav2lip_original(imagen, audio, salida)
        
        if resultado:
            print(f"\n✅ Video generado: {salida}")
        else:
            print("\n❌ Error en generación")
            print("💡 Asegúrate de tener el modelo wav2lip_gan.pth")
            
    except ImportError as e:
        print(f"❌ Error importando: {e}")

def main():
    """Función principal"""
    while True:
        mostrar_menu()
        
        try:
            opcion = input("Selecciona una opción (1-6): ").strip()
            
            if opcion == "1":
                ejecutar_wav2lip_simple()
            elif opcion == "2":
                ejecutar_wav2lip_mejorado()
            elif opcion == "3":
                ejecutar_wav2lip_original()
            elif opcion == "4":
                crear_audio_personalizado()
            elif opcion == "5":
                listar_archivos()
            elif opcion == "6":
                print("👋 ¡Hasta luego!")
                break
            else:
                print("❌ Opción inválida")
            
            input("\n📱 Presiona Enter para continuar...")
            print("\n" + "="*50 + "\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 ¡Hasta luego!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            input("\n📱 Presiona Enter para continuar...")

if __name__ == "__main__":
    main()