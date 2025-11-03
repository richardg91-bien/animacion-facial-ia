"""
Script para usar Wav2Lip original con modificaciones para compatibilidad
"""

import os
import sys
import subprocess
from pathlib import Path

def setup_wav2lip_original():
    """Configurar Wav2Lip original para uso"""
    print("🔧 Configurando Wav2Lip original...")
    
    wav2lip_dir = Path("Wav2Lip")
    if not wav2lip_dir.exists():
        print("❌ Directorio Wav2Lip no encontrado")
        return False
    
    # Verificar archivos necesarios
    inference_file = wav2lip_dir / "inference.py"
    if not inference_file.exists():
        print("❌ inference.py no encontrado")
        return False
    
    # Crear directorio de checkpoints si no existe
    checkpoints_dir = wav2lip_dir / "checkpoints"
    checkpoints_dir.mkdir(exist_ok=True)
    
    # Verificar si existe el modelo preentrenado
    model_path = checkpoints_dir / "wav2lip_gan.pth"
    if not model_path.exists():
        print("⚠️  Modelo wav2lip_gan.pth no encontrado")
        print("💡 Descargando modelo preentrenado...")
        
        # URL del modelo (esta es una URL de ejemplo, necesitarías la real)
        model_url = "https://iiitaphyd-my.sharepoint.com/personal/radrabha_m_research_iiit_ac_in/_layouts/15/download.aspx?share=EdjI7bZlgApMqsVoEUUXpLsBxqXbn5z8VTmoxp2pgQ7MWQ"
        
        print("🌐 Intentando descargar modelo...")
        print("💡 Nota: Debes descargar manualmente wav2lip_gan.pth del repositorio oficial")
        print("🔗 Link: https://github.com/Rudrabha/Wav2Lip#getting-the-weights")
        
        return False
    
    print("✅ Wav2Lip original configurado")
    return True

def run_wav2lip_original(face_image, audio_file, output_path="result_original.mp4"):
    """Ejecutar Wav2Lip original"""
    print("🎬 Ejecutando Wav2Lip original...")
    
    if not setup_wav2lip_original():
        print("❌ Error en configuración")
        return False
    
    # Cambiar al directorio de Wav2Lip
    original_dir = os.getcwd()
    wav2lip_dir = Path("Wav2Lip")
    
    try:
        os.chdir(wav2lip_dir)
        
        # Comando para ejecutar inference
        cmd = [
            "python", "inference.py",
            "--checkpoint_path", "checkpoints/wav2lip_gan.pth",
            "--face", f"../{face_image}",
            "--audio", f"../{audio_file}",
            "--outfile", f"../{output_path}"
        ]
        
        print(f"🚀 Ejecutando: {' '.join(cmd)}")
        
        # Ejecutar comando
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Video generado: {output_path}")
            return True
        else:
            print("❌ Error en ejecución:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        os.chdir(original_dir)

def main():
    """Demo del Wav2Lip original"""
    print("🎭 WAV2LIP ORIGINAL - WRAPPER")
    print("=" * 40)
    
    # Archivos
    imagen = "woman-3584435_1280.jpg"
    audio = "hola_ejemplo.wav"
    
    if not os.path.exists(imagen):
        print(f"❌ Imagen no encontrada: {imagen}")
        return
    
    if not os.path.exists(audio):
        print(f"❌ Audio no encontrado: {audio}")
        return
    
    # Intentar ejecutar Wav2Lip original
    resultado = run_wav2lip_original(imagen, audio, "wav2lip_original.mp4")
    
    if resultado:
        print("\n🎉 ¡Video original generado!")
    else:
        print("\n⚠️  No se pudo ejecutar Wav2Lip original")
        print("💡 Usa wav2lip_simple.py o wav2lip_mejorado.py como alternativa")

if __name__ == "__main__":
    main()