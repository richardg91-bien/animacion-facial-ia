# 🎭 WAV2LIP CLI - Guía de Uso

## 📋 Descripción
Script de línea de comandos para generar videos con sincronización de labios sin interfaz gráfica.

## 🚀 Instalación de Dependencias

```bash
# Instalar dependencias desde requirements.txt
pip install -r requirements.txt

# O instalar manualmente las principales:
pip install opencv-python mediapipe torch pyttsx3 ffmpeg-python
```

## 💻 Uso del Script

### Modo Test (Recomendado para primera prueba)
```bash
python wav2lip_cli.py --test
```

### Uso con Archivos Personalizados
```bash
python wav2lip_cli.py --imagen tu_imagen.jpg --texto "Tu texto aquí"
```

### Especificar Archivo de Salida
```bash
python wav2lip_cli.py --imagen foto.png --texto "Hola mundo" --salida mi_video.mp4
```

## 📖 Ejemplos Completos

### Ejemplo 1: Básico
```bash
python wav2lip_cli.py --imagen woman-3584435_1280.jpg --texto "Hola, este es un ejemplo básico"
```

### Ejemplo 2: Con salida personalizada
```bash
python wav2lip_cli.py \
  --imagen mi_foto.jpg \
  --texto "Este es un mensaje más largo para probar la sincronización" \
  --salida resultados/mi_video_personalizado.mp4
```

### Ejemplo 3: Texto largo
```bash
python wav2lip_cli.py \
  --imagen rostro.png \
  --texto "Este es un ejemplo de texto más extenso que demuestra las capacidades del sistema de sincronización de labios utilizando inteligencia artificial y procesamiento de audio en tiempo real"
```

## 📁 Estructura de Archivos Generados

```
resultados/
├── [nombre_imagen]_audio.wav      # Audio generado desde texto
├── [nombre_imagen]_cartoon.jpg    # Imagen con efecto cartoon
└── [nombre_imagen]_final.mp4      # Video final con lip-sync
```

## 🔧 Requisitos del Sistema

### Software Necesario
- **Python 3.8+** (probado en 3.12)
- **FFmpeg** (para procesamiento de video)
- **Entorno virtual** (recomendado)

### Formatos Soportados
- **Imágenes**: JPG, JPEG, PNG, BMP
- **Video de salida**: MP4 (H.264)
- **Audio interno**: WAV

## ⚡ Características

### ✅ Lo que SÍ hace
- ✅ Genera audio desde texto (TTS con pyttsx3)
- ✅ Detecta caras automáticamente (OpenCV)
- ✅ Aplica efectos cartoon opcionales
- ✅ Combina imagen y audio en video MP4
- ✅ Funciona sin interfaz gráfica
- ✅ Acepta argumentos por línea de comandos

### ⚠️ Limitaciones
- ⚠️ Lip-sync básico (no usa IA avanzada como WAV2LIP original)
- ⚠️ Una cara por imagen recomendado
- ⚠️ Requiere FFmpeg instalado en el sistema
- ⚠️ Calidad de sincronización depende de la claridad de la imagen

## 🔍 Solución de Problemas

### Error: "ffmpeg no encontrado"
```bash
# Windows: Descargar desde https://ffmpeg.org/
# Agregar FFmpeg al PATH del sistema
# Verificar: ffmpeg -version
```

### Error: "No se detectaron caras"
- Usar imagen con cara claramente visible
- Buena iluminación en la foto
- Cara frontal o ligeramente ladeada

### Error: "Dependencias faltantes"
```bash
pip install -r requirements.txt
```

## 📊 Rendimiento

### Tiempo Aproximado de Procesamiento
- **Imagen 1080p + 10s audio**: ~30-60 segundos
- **Imagen 4K + 30s audio**: ~2-5 minutos

### Optimización
- Usar imágenes de resolución media (1080p máximo)
- Textos de 10-30 segundos para mejores resultados
- Cerrar otras aplicaciones durante el procesamiento

## 🎯 Próximas Mejoras

- [ ] Integración con modelos WAV2LIP avanzados
- [ ] Soporte para múltiples caras
- [ ] Procesamiento en lotes
- [ ] Optimización de velocidad
- [ ] Más efectos de imagen

---

**¡Disfruta creando videos con sincronización de labios desde la línea de comandos! 🎬✨**