#!/usr/bin/env python3
"""
WAV2LIP DOCKER SETUP - Configuración para contenedor Docker
Este script prepara todo para ejecutar en un entorno Docker con todas las dependencias
"""

import os
import json
from pathlib import Path

def crear_dockerfile():
    """Crear Dockerfile con todas las dependencias"""
    dockerfile_content = """# WAV2LIP Docker Environment
FROM python:3.12-slim

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \\
    ffmpeg \\
    libgl1-mesa-glx \\
    libglib2.0-0 \\
    libsm6 \\
    libxext6 \\
    libxrender-dev \\
    libgomp1 \\
    libgstreamer1.0-0 \\
    gstreamer1.0-plugins-base \\
    gstreamer1.0-plugins-good \\
    && rm -rf /var/lib/apt/lists/*

# Establecer directorio de trabajo
WORKDIR /app

# Copiar requirements.txt
COPY requirements.txt .

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar archivos del proyecto
COPY . .

# Comando por defecto
CMD ["python", "wav2lip_cli.py", "--help"]
"""
    
    with open("Dockerfile", "w") as f:
        f.write(dockerfile_content)
    
    print("✅ Dockerfile creado")

def crear_docker_compose():
    """Crear docker-compose.yml para fácil ejecución"""
    compose_content = """version: '3.8'

services:
  wav2lip:
    build: .
    volumes:
      - ./resultados:/app/resultados
      - ./input:/app/input
    environment:
      - PYTHONUNBUFFERED=1
    command: python wav2lip_cli.py --test

  wav2lip-custom:
    build: .
    volumes:
      - ./resultados:/app/resultados
      - ./input:/app/input
    environment:
      - PYTHONUNBUFFERED=1
    command: python wav2lip_cli.py --imagen input/imagen.jpg --texto "Tu texto aquí"
"""
    
    with open("docker-compose.yml", "w") as f:
        f.write(compose_content)
    
    print("✅ docker-compose.yml creado")

def crear_scripts_ejecucion():
    """Crear scripts para diferentes plataformas"""
    
    # Script Windows
    windows_script = """@echo off
echo 🐳 Ejecutando WAV2LIP en Docker...

REM Crear directorios necesarios
if not exist "input" mkdir input
if not exist "resultados" mkdir resultados

REM Construir imagen Docker
docker build -t wav2lip-app .

REM Ejecutar en modo test
docker run --rm -v "%cd%\\resultados:/app/resultados" wav2lip-app python wav2lip_cli.py --test

echo ✅ Proceso completado. Revisa la carpeta 'resultados'
pause
"""
    
    with open("ejecutar_docker.bat", "w") as f:
        f.write(windows_script)
    
    # Script Linux/Mac
    linux_script = """#!/bin/bash
echo "🐳 Ejecutando WAV2LIP en Docker..."

# Crear directorios necesarios
mkdir -p input
mkdir -p resultados

# Construir imagen Docker
docker build -t wav2lip-app .

# Ejecutar en modo test
docker run --rm -v "$(pwd)/resultados:/app/resultados" wav2lip-app python wav2lip_cli.py --test

echo "✅ Proceso completado. Revisa la carpeta 'resultados'"
"""
    
    with open("ejecutar_docker.sh", "w") as f:
        f.write(linux_script)
    
    # Hacer ejecutable en Linux/Mac
    os.chmod("ejecutar_docker.sh", 0o755)
    
    print("✅ Scripts de ejecución creados")

def crear_requirements_docker():
    """Crear requirements específico para Docker"""
    requirements = """# WAV2LIP Dependencies for Docker
opencv-python-headless==4.12.0.88
mediapipe==0.10.21
torch==2.9.0+cpu
torchvision==0.24.0+cpu
torchaudio==2.9.0+cpu
pyttsx3==2.99
pillow==12.0.0
numpy==1.26.4
scipy==1.16.3
matplotlib==3.10.7
tqdm==4.67.1
ffmpeg-python==0.2.0
argparse
"""
    
    with open("requirements-docker.txt", "w") as f:
        f.write(requirements)
    
    print("✅ requirements-docker.txt creado")

def crear_guia_docker():
    """Crear guía de uso con Docker"""
    guia = """# 🐳 WAV2LIP con Docker - Guía Completa

## 📋 Prerequisitos
- Docker Desktop instalado
- Git (para clonar el proyecto)

## 🚀 Instalación y Uso

### 1. Preparar el Proyecto
```bash
# Clonar el repositorio
git clone [tu-repositorio]
cd animacion_integrado_mejorado

# Crear directorios necesarios
mkdir -p input resultados
```

### 2. Ejecutar con Docker

#### Opción A: Script Automático (Recomendado)
```bash
# Windows
ejecutar_docker.bat

# Linux/Mac
./ejecutar_docker.sh
```

#### Opción B: Docker Compose
```bash
# Modo test
docker-compose up wav2lip

# Con imagen personalizada (coloca tu imagen en ./input/)
docker-compose up wav2lip-custom
```

#### Opción C: Comandos Docker Manuales
```bash
# Construir imagen
docker build -t wav2lip-app .

# Ejecutar modo test
docker run --rm -v "$(pwd)/resultados:/app/resultados" wav2lip-app python wav2lip_cli.py --test

# Ejecutar con imagen personalizada
docker run --rm \\
  -v "$(pwd)/input:/app/input" \\
  -v "$(pwd)/resultados:/app/resultados" \\
  wav2lip-app \\
  python wav2lip_cli.py --imagen input/tu_imagen.jpg --texto "Tu mensaje aquí"
```

## 📁 Estructura de Archivos

```
proyecto/
├── Dockerfile              # Configuración del contenedor
├── docker-compose.yml      # Orquestación de servicios
├── requirements-docker.txt # Dependencias específicas
├── ejecutar_docker.bat     # Script Windows
├── ejecutar_docker.sh      # Script Linux/Mac
├── input/                  # Tus imágenes de entrada
│   └── tu_imagen.jpg
├── resultados/             # Videos generados
│   └── output.mp4
└── wav2lip_cli.py          # Script principal
```

## 🎯 Ventajas de Docker

✅ **Aislamiento completo** - No afecta tu sistema
✅ **Dependencias garantizadas** - OpenCV, MediaPipe, PyTorch incluidos
✅ **Reproducible** - Funciona igual en cualquier máquina
✅ **Fácil distribución** - Compartir solo requiere Docker
✅ **Sin conflictos** - No interfiere con otros proyectos

## 🔧 Personalización

### Cambiar la Imagen Base
```dockerfile
# En Dockerfile, cambiar:
FROM python:3.12-slim
# Por:
FROM python:3.11-slim
```

### Agregar Más Dependencias
```bash
# Editar requirements-docker.txt
echo "nueva-libreria==1.0.0" >> requirements-docker.txt
```

### Usar GPU (si disponible)
```dockerfile
# Cambiar imagen base por:
FROM pytorch/pytorch:2.0.0-cuda11.7-cudnn8-runtime
```

## 🚨 Solución de Problemas

### Error: "Docker no encontrado"
```bash
# Instalar Docker Desktop desde:
# https://www.docker.com/products/docker-desktop
```

### Error: "Permisos denegados"
```bash
# Linux/Mac - Dar permisos al script:
chmod +x ejecutar_docker.sh
```

### Error: "Puerto ocupado"
```bash
# Limpiar contenedores:
docker system prune -f
```

## 📊 Rendimiento Esperado

- **Primera ejecución**: ~5-10 minutos (descarga dependencias)
- **Ejecuciones posteriores**: ~30-60 segundos
- **Tamaño imagen**: ~2-3 GB
- **RAM requerida**: ~2-4 GB

---

**¡Con Docker tendrás WAV2LIP funcionando en cualquier sistema! 🎬✨**
"""
    
    with open("DOCKER_README.md", "w") as f:
        f.write(guia)
    
    print("✅ DOCKER_README.md creado")

def main():
    """Función principal"""
    print("🐳 WAV2LIP DOCKER SETUP")
    print("=" * 40)
    
    print("📦 Creando archivos Docker...")
    crear_dockerfile()
    crear_docker_compose()
    crear_scripts_ejecucion()
    crear_requirements_docker()
    crear_guia_docker()
    
    print("\n🎉 ¡Setup Docker completado!")
    print("\n📋 Archivos creados:")
    print("   - Dockerfile")
    print("   - docker-compose.yml") 
    print("   - ejecutar_docker.bat (Windows)")
    print("   - ejecutar_docker.sh (Linux/Mac)")
    print("   - requirements-docker.txt")
    print("   - DOCKER_README.md")
    
    print("\n🚀 Para usar:")
    print("   1. Instala Docker Desktop")
    print("   2. Ejecuta: ./ejecutar_docker.sh (o .bat en Windows)")
    print("   3. ¡Docker se encarga del resto!")

if __name__ == "__main__":
    main()