#!/usr/bin/env python3
"""
Diagnóstico del entorno - Verificar qué librerías están disponibles
"""

import sys
import importlib
import platform
import os

def verificar_libreria(nombre, importar_como=None):
    """Verificar si una librería está disponible"""
    try:
        if importar_como:
            modulo = importlib.import_module(importar_como)
        else:
            modulo = importlib.import_module(nombre)
        
        version = getattr(modulo, '__version__', 'Desconocida')
        return True, version
    except ImportError:
        return False, None

def diagnostico_completo():
    """Ejecutar diagnóstico completo del entorno"""
    print("🔍 DIAGNÓSTICO DEL ENTORNO")
    print("=" * 50)
    
    # Información del sistema
    print(f"🖥️  Sistema: {platform.system()} {platform.release()}")
    print(f"🐍 Python: {sys.version}")
    print(f"📍 Ejecutable: {sys.executable}")
    print(f"📂 Directorio actual: {os.getcwd()}")
    
    # Librerías a verificar
    librerias = [
        ("PIL", "PIL"),
        ("OpenCV", "cv2"), 
        ("MediaPipe", "mediapipe"),
        ("PyTorch", "torch"),
        ("NumPy", "numpy"),
        ("pyttsx3", "pyttsx3"),
        ("ffmpeg-python", "ffmpeg"),
        ("matplotlib", "matplotlib"),
        ("tqdm", "tqdm"),
        ("argparse", "argparse"),
        ("json", "json"),
        ("subprocess", "subprocess"),
        ("pathlib", "pathlib")
    ]
    
    print(f"\n📦 VERIFICACIÓN DE LIBRERÍAS:")
    print("-" * 30)
    
    disponibles = []
    no_disponibles = []
    
    for nombre, modulo in librerias:
        esta, version = verificar_libreria(nombre, modulo)
        if esta:
            print(f"✅ {nombre:<15} - v{version}")
            disponibles.append(nombre)
        else:
            print(f"❌ {nombre:<15} - No disponible")
            no_disponibles.append(nombre)
    
    # Resumen
    print(f"\n📊 RESUMEN:")
    print(f"✅ Disponibles: {len(disponibles)}")
    print(f"❌ Faltantes: {len(no_disponibles)}")
    
    # Recomendaciones
    print(f"\n💡 RECOMENDACIONES:")
    
    if len(no_disponibles) == 0:
        print("🎉 ¡Todas las librerías están disponibles!")
        print("🚀 Puedes usar wav2lip_cli.py sin problemas")
    
    elif "PIL" in disponibles and "argparse" in disponibles:
        print("✅ Librerías básicas disponibles")
        print("🔧 Puedes usar wav2lip_minimal.py")
        
    elif "argparse" in disponibles:
        print("⚠️  Solo librerías estándar disponibles")
        print("📋 Usar modo diagnóstico y scripts generados")
    
    else:
        print("❌ Entorno muy limitado")
        print("📋 Solo análisis de metadatos posible")
    
    # Verificar archivos del proyecto
    print(f"\n📁 ARCHIVOS DEL PROYECTO:")
    archivos_proyecto = [
        "wav2lip_cli.py",
        "wav2lip_minimal.py", 
        "requirements.txt",
        "woman-3584435_1280.jpg",
        "CLI_README.md"
    ]
    
    for archivo in archivos_proyecto:
        if os.path.exists(archivo):
            tamaño = os.path.getsize(archivo)
            print(f"✅ {archivo:<25} ({tamaño:,} bytes)")
        else:
            print(f"❌ {archivo:<25} - No encontrado")
    
    return {
        "disponibles": disponibles,
        "no_disponibles": no_disponibles,
        "python_version": sys.version,
        "sistema": platform.system()
    }

if __name__ == "__main__":
    resultado = diagnostico_completo()
    
    # Guardar diagnóstico
    import json
    with open("diagnostico_entorno.json", "w") as f:
        json.dump(resultado, f, indent=2)
    
    print(f"\n💾 Diagnóstico guardado en: diagnostico_entorno.json")