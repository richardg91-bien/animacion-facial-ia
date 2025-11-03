import pyttsx3
import os

def crear_audio_ejemplo():
    """Crear un archivo de audio de ejemplo"""
    print("🎤 Creando audio de ejemplo...")
    
    engine = pyttsx3.init()
    
    # Configurar voz
    voices = engine.getProperty('voices')
    if voices:
        # Usar voz femenina si está disponible
        for voice in voices:
            if 'female' in voice.name.lower() or 'helena' in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break
    
    # Configurar velocidad
    engine.setProperty('rate', 150)  # Velocidad de habla
    
    # Texto a convertir
    texto = "Hola, soy un ejemplo de sincronización de labios con inteligencia artificial. Esto demuestra cómo se puede animar una imagen estática."
    
    # Guardar audio
    audio_file = "hola_ejemplo.wav"
    engine.save_to_file(texto, audio_file)
    engine.runAndWait()
    
    if os.path.exists(audio_file):
        print(f"✅ Audio creado: {audio_file}")
        return audio_file
    else:
        print("❌ Error creando audio")
        return None

if __name__ == "__main__":
    crear_audio_ejemplo()