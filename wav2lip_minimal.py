#!/usr/bin/env python3
"""
WAV2LIP MINIMAL CLI - Versión ultra minimalista
Solo usa librerías estándar de Python + PIL básico
Para entornos con dependencias limitadas
"""

import argparse
import os
import sys
import subprocess
from pathlib import Path

# Solo librerías estándar
import json
import time
from datetime import datetime

# Configuración
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(BASE_DIR, "resultados")
os.makedirs(RESULTS_DIR, exist_ok=True)

def crear_audio_simple(texto, output_path):
    """
    Crear audio usando herramientas del sistema
    """
    print(f"🎤 Generando audio: '{texto[:50]}...'")
    
    # Opción 1: Intentar con PowerShell en Windows
    if os.name == 'nt':  # Windows
        try:
            ps_script = f'''
Add-Type -AssemblyName System.Speech
$speak = New-Object System.Speech.Synthesis.SpeechSynthesizer
$speak.SetOutputToWaveFile("{output_path}")
$speak.Speak("{texto}")
$speak.Dispose()
'''
            with open("temp_tts.ps1", "w", encoding="utf-8") as f:
                f.write(ps_script)
            
            result = subprocess.run(
                ["powershell", "-ExecutionPolicy", "Bypass", "-File", "temp_tts.ps1"],
                capture_output=True, text=True
            )
            
            os.remove("temp_tts.ps1")
            
            if os.path.exists(output_path):
                print(f"✅ Audio generado con PowerShell: {output_path}")
                return True
                
        except Exception as e:
            print(f"⚠️  PowerShell TTS falló: {e}")
    
    # Opción 2: Crear archivo de metadatos en lugar de audio real
    metadata = {
        "texto": texto,
        "timestamp": datetime.now().isoformat(),
        "duracion_estimada": len(texto.split()) * 0.5,  # ~0.5s por palabra
        "archivo_audio": output_path
    }
    
    metadata_path = output_path.replace(".wav", "_metadata.json")
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    print(f"📋 Metadatos de audio creados: {metadata_path}")
    return True

def procesar_imagen_basico(imagen_path, output_path):
    """
    Procesamiento básico de imagen usando PIL o info
    """
    print("🖼️  Analizando imagen...")
    
    try:
        # Intentar con PIL si está disponible
        try:
            from PIL import Image, ImageEnhance, ImageFilter
            
            img = Image.open(imagen_path)
            print(f"✅ Imagen cargada: {img.size} pixels, modo: {img.mode}")
            
            # Aplicar efectos básicos
            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance(1.2)
            
            img = img.filter(ImageFilter.SMOOTH)
            
            img.save(output_path, "JPEG", quality=85)
            print(f"✅ Imagen procesada guardada: {output_path}")
            return True
            
        except ImportError:
            print("⚠️  PIL no disponible, creando metadatos...")
            
            # Crear metadatos de imagen
            metadata = {
                "imagen_original": imagen_path,
                "timestamp": datetime.now().isoformat(),
                "procesamiento": "metadata_only",
                "existe": os.path.exists(imagen_path)
            }
            
            metadata_path = output_path.replace(".jpg", "_metadata.json")
            with open(metadata_path, "w", encoding="utf-8") as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            
            print(f"📋 Metadatos de imagen creados: {metadata_path}")
            return True
            
    except Exception as e:
        print(f"❌ Error procesando imagen: {e}")
        return False

def crear_script_video(imagen_path, audio_path, output_path):
    """
    Crear script para generar video (sin ejecutar)
    """
    print("🎬 Generando script de video...")
    
    script_content = f"""#!/bin/bash
# Script generado automáticamente para crear video

# Comando FFmpeg para combinar imagen y audio
ffmpeg -y \\
  -loop 1 \\
  -i "{imagen_path}" \\
  -i "{audio_path}" \\
  -c:v libx264 \\
  -tune stillimage \\
  -c:a aac \\
  -b:a 192k \\
  -pix_fmt yuv420p \\
  -shortest \\
  "{output_path}"

echo "Video creado: {output_path}"
"""
    
    script_path = output_path.replace(".mp4", "_script.sh")
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(script_content)
    
    # También crear versión PowerShell
    ps_content = f"""# Script PowerShell para crear video
$ffmpeg_cmd = @"
ffmpeg -y -loop 1 -i "{imagen_path}" -i "{audio_path}" -c:v libx264 -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -shortest "{output_path}"
"@

Write-Host "Ejecutar comando:"
Write-Host $ffmpeg_cmd
Write-Host ""
Write-Host "Si tienes FFmpeg instalado, ejecuta el comando anterior."
"""
    
    ps_path = output_path.replace(".mp4", "_script.ps1")
    with open(ps_path, "w", encoding="utf-8") as f:
        f.write(ps_content)
    
    print(f"✅ Scripts generados:")
    print(f"   🐧 Bash: {script_path}")
    print(f"   🪟 PowerShell: {ps_path}")
    
    return True

def simular_wav2lip(imagen_path, texto, output_path):
    """
    Simulación del proceso WAV2LIP sin dependencias pesadas
    """
    print("🎭 INICIANDO WAV2LIP MINIMAL")
    print("=" * 50)
    
    # Validar entrada
    if not os.path.exists(imagen_path):
        print(f"❌ Imagen no encontrada: {imagen_path}")
        return False
    
    print(f"✅ Imagen: {imagen_path}")
    print(f"🎤 Texto: '{texto}'")
    print(f"📹 Salida: {output_path}")
    
    # Nombres de archivos temporales
    base_name = Path(imagen_path).stem
    audio_path = os.path.join(RESULTS_DIR, f"{base_name}_audio.wav")
    imagen_proc = os.path.join(RESULTS_DIR, f"{base_name}_processed.jpg")
    
    # Proceso simulado
    steps = [
        ("🎤 Generando audio...", lambda: crear_audio_simple(texto, audio_path)),
        ("🖼️  Procesando imagen...", lambda: procesar_imagen_basico(imagen_path, imagen_proc)),
        ("🎬 Creando scripts de video...", lambda: crear_script_video(imagen_path, audio_path, output_path))
    ]
    
    for i, (desc, func) in enumerate(steps, 1):
        print(f"\n📁 PASO {i}/3: {desc}")
        if not func():
            print(f"❌ Error en paso {i}")
            return False
        time.sleep(0.5)  # Simular procesamiento
    
    # Crear informe final
    informe = {
        "timestamp": datetime.now().isoformat(),
        "imagen_entrada": imagen_path,
        "texto_procesado": texto,
        "archivos_generados": {
            "audio": audio_path if os.path.exists(audio_path) else f"{audio_path}_metadata.json",
            "imagen_procesada": imagen_proc if os.path.exists(imagen_proc) else f"{imagen_proc}_metadata.json",
            "script_bash": output_path.replace(".mp4", "_script.sh"),
            "script_powershell": output_path.replace(".mp4", "_script.ps1")
        },
        "estado": "completado_simulacion",
        "notas": "Procesamiento realizado sin dependencias pesadas. Usar scripts generados para crear video final."
    }
    
    informe_path = output_path.replace(".mp4", "_informe.json")
    with open(informe_path, "w", encoding="utf-8") as f:
        json.dump(informe, f, indent=2, ensure_ascii=False)
    
    print(f"\n🎉 ¡PROCESO COMPLETADO!")
    print(f"📋 Informe: {informe_path}")
    print(f"📂 Revisa la carpeta 'resultados' para ver todos los archivos generados.")
    print(f"\n💡 Para crear el video final:")
    print(f"   1. Instala FFmpeg si no lo tienes")
    print(f"   2. Ejecuta el script generado")
    
    return True

def main():
    parser = argparse.ArgumentParser(
        description="🎭 WAV2LIP MINIMAL CLI - Versión sin dependencias pesadas",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Esta versión minimalista:
- ✅ Funciona solo con Python estándar + PIL opcional
- ✅ Genera scripts para crear video con FFmpeg
- ✅ Crea metadatos detallados del proceso
- ⚠️  No hace lip-sync real (requiere IA avanzada)

Ejemplos:
  python wav2lip_minimal.py --test
  python wav2lip_minimal.py --imagen foto.jpg --texto "Hola mundo"
        """
    )
    
    parser.add_argument('--imagen', type=str, help='Ruta a la imagen')
    parser.add_argument('--texto', type=str, help='Texto para generar audio')
    parser.add_argument('--salida', type=str, help='Archivo de salida')
    parser.add_argument('--test', action='store_true', help='Modo test')
    
    args = parser.parse_args()
    
    if args.test:
        print("🧪 MODO TEST")
        imagen = os.path.join(BASE_DIR, "woman-3584435_1280.jpg")
        texto = "Esto es una prueba del sistema minimal sin dependencias pesadas"
        salida = os.path.join(RESULTS_DIR, "test_minimal.mp4")
        
        if not os.path.exists(imagen):
            print(f"❌ Archivo test no encontrado: {imagen}")
            return False
            
        return simular_wav2lip(imagen, texto, salida)
    
    if not args.imagen or not args.texto:
        parser.error("Se requieren --imagen y --texto (o usar --test)")
    
    if not args.salida:
        base_name = Path(args.imagen).stem
        args.salida = os.path.join(RESULTS_DIR, f"{base_name}_minimal.mp4")
    
    return simular_wav2lip(args.imagen, args.texto, args.salida)

if __name__ == '__main__':
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⚠️  Interrumpido por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)