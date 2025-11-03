"""
WAV2LIP_COLAB.ipynb - Notebook para Google Colab
Copia este contenido en un nuevo notebook de Colab
"""

colab_notebook = {
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# 🎭 WAV2LIP en Google Colab\n",
                "\n",
                "Este notebook ejecuta WAV2LIP con todas las dependencias en la nube.\n",
                "\n",
                "## 🚀 Ventajas de Colab:\n",
                "- ✅ Todas las librerías disponibles\n",
                "- ✅ GPU gratuita disponible  \n",
                "- ✅ No requiere instalación local\n",
                "- ✅ Funciona desde cualquier navegador"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "source": [
                "# 📦 PASO 1: Instalar dependencias\n",
                "!pip install opencv-python mediapipe torch torchvision torchaudio pyttsx3 pillow ffmpeg-python tqdm\n",
                "\n",
                "# Verificar instalación\n",
                "import cv2\n",
                "import mediapipe\n",
                "import torch\n",
                "print(f\"✅ OpenCV: {cv2.__version__}\")\n",
                "print(f\"✅ MediaPipe: {mediapipe.__version__}\")\n",
                "print(f\"✅ PyTorch: {torch.__version__}\")"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "source": [
                "# 📁 PASO 2: Clonar el proyecto\n",
                "!git clone https://github.com/tu-usuario/tu-repositorio.git\n",
                "%cd tu-repositorio\n",
                "\n",
                "# Listar archivos\n",
                "!ls -la"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "source": [
                "# 🎬 PASO 3: Ejecutar WAV2LIP\n",
                "!python wav2lip_cli.py --test"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "source": [
                "# 📤 PASO 4: Subir tu propia imagen\n",
                "from google.colab import files\n",
                "import os\n",
                "\n",
                "print(\"📤 Sube tu imagen:\")\n",
                "uploaded = files.upload()\n",
                "\n",
                "# Obtener nombre del archivo subido\n",
                "imagen_subida = list(uploaded.keys())[0]\n",
                "print(f\"✅ Imagen subida: {imagen_subida}\")"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "source": [
                "# 🎤 PASO 5: Procesar con tu imagen y texto\n",
                "texto_personalizado = \"Escribe aquí el texto que quieres que diga la persona en la imagen\"\n",
                "\n",
                "!python wav2lip_cli.py --imagen {imagen_subida} --texto \"{texto_personalizado}\""
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "source": [
                "# 📁 PASO 6: Ver resultados\n",
                "!ls -la resultados/\n",
                "\n",
                "# Mostrar video generado\n",
                "from IPython.display import Video\n",
                "import glob\n",
                "\n",
                "# Buscar el video más reciente\n",
                "videos = glob.glob(\"resultados/*.mp4\")\n",
                "if videos:\n",
                "    video_mas_reciente = max(videos, key=os.path.getctime)\n",
                "    print(f\"🎬 Reproduciendo: {video_mas_reciente}\")\n",
                "    Video(video_mas_reciente, width=640, height=480)\n",
                "else:\n",
                "    print(\"❌ No se encontraron videos\")"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "source": [
                "# 📥 PASO 7: Descargar resultados\n",
                "from google.colab import files\n",
                "import zipfile\n",
                "\n",
                "# Crear ZIP con todos los resultados\n",
                "with zipfile.ZipFile('wav2lip_resultados.zip', 'w') as zipf:\n",
                "    for root, dirs, files in os.walk('resultados'):\n",
                "        for file in files:\n",
                "            file_path = os.path.join(root, file)\n",
                "            zipf.write(file_path)\n",
                "\n",
                "print(\"📦 Descargando archivo ZIP con resultados...\")\n",
                "files.download('wav2lip_resultados.zip')"
            ]
        }
    ],
    "metadata": {
        "colab": {
            "provenance": []
        },
        "kernelspec": {
            "display_name": "Python 3",
            "name": "python3"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 0
}

# Guardar como archivo JSON que puede ser importado a Colab
import json

with open("WAV2LIP_COLAB.ipynb", "w", encoding="utf-8") as f:
    json.dump(colab_notebook, f, indent=2, ensure_ascii=False)

print("✅ Notebook de Colab creado: WAV2LIP_COLAB.ipynb")
print("\n🚀 Para usar:")
print("1. Ve a https://colab.research.google.com/")  
print("2. Sube el archivo WAV2LIP_COLAB.ipynb")
print("3. Ejecuta las celdas paso a paso")
print("4. ¡Todas las dependencias estarán disponibles!")