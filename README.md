# 🎭 WAV2LIP SUITE - Sincronización de Labios con IA

Sistema completo de sincronización de labios (lip-sync) que permite animar imágenes estáticas con audio, creando videos donde la persona parece hablar naturalmente.

## 🌟 Características

- **3 Implementaciones Diferentes**: Simple, Mejorada y Original
- **Detección Automática de Caras**: Usando OpenCV
- **Sincronización con Audio**: Análisis de características de voz
- **Generación de Video**: Combina imagen + audio = video animado
- **Interface Interactiva**: Menú fácil de usar

## 📋 Requisitos

### Software Necesario
- Python 3.10+ (probado en 3.14)
- FFmpeg (para procesamiento de video/audio)
- Entorno virtual Python

### Dependencias Python
```bash
pip install opencv-python
pip install torch torchvision torchaudio
pip install pyttsx3
pip install tqdm
pip install numpy
pip install pillow
```

## 🚀 Instalación

1. **Clonar/Descargar** este proyecto
2. **Activar entorno virtual**:
   ```bash
   .\env\Scripts\Activate.ps1  # Windows PowerShell
   ```
3. **Instalar dependencias** (ya instaladas en tu entorno)
4. **Verificar FFmpeg**:
   ```bash
   ffmpeg -version
   ```

## 📁 Estructura del Proyecto

```
animacion/
├── wav2lip_suite.py           # 🎮 Menú principal
├── wav2lip_simple.py          # 🚀 Versión simple
├── wav2lip_mejorado.py        # 🎨 Versión mejorada
├── wav2lip_original_wrapper.py # 🔥 Wrapper para original
├── crear_audio.py             # 🎤 Generador de audio
├── cartoonizar.py             # 🎨 Cartoonización (bonus)
├── woman-3584435_1280.jpg     # 🖼️ Imagen de ejemplo
├── hola_ejemplo.wav           # 🎵 Audio de ejemplo
└── Wav2Lip/                   # 📂 Repositorio original
```

## 🎮 Uso Rápido

### Método 1: Suite Interactiva (Recomendado)
```bash
python wav2lip_suite.py
```
Te guiará paso a paso a través de todas las opciones.

### Método 2: Scripts Individuales

#### Wav2Lip Simple (Rápido)
```bash
python wav2lip_simple.py
```

#### Wav2Lip Mejorado (Mejor calidad)
```bash
python wav2lip_mejorado.py
```

## 🎯 Ejemplos de Uso

### Ejemplo Básico
```python
from wav2lip_simple import Wav2LipSimple

wav2lip = Wav2LipSimple()
wav2lip.create_video_from_image(
    image_path="mujer.jpg",
    audio_path="hola.wav", 
    output_path="resultado.mp4"
)
```

### Ejemplo Avanzado
```python
from wav2lip_mejorado import Wav2LipMejorado

wav2lip = Wav2LipMejorado()
wav2lip.create_video_from_image_advanced(
    image_path="mujer.jpg",
    audio_path="discurso.wav",
    output_path="discurso_animado.mp4"
)
```

## 📊 Comparación de Versiones

| Característica | Simple | Mejorada | Original |
|---------------|--------|----------|----------|
| **Velocidad** | ⚡ Muy rápida | 🏃 Rápida | 🐌 Lenta |
| **Calidad** | ✅ Básica | 🎨 Buena | 🔥 Excelente |
| **Requisitos** | 📦 Mínimos | 🔧 Moderados | 💾 Altos |
| **Dependencias** | 🟢 Pocas | 🟡 Moderadas | 🔴 Muchas |
| **Compatibilidad** | ✅ Universal | ✅ Universal | ⚠️ Limitada |

## 🎤 Crear Audio Personalizado

### Opción 1: Desde la Suite
```bash
python wav2lip_suite.py
# Selecciona opción 4
```

### Opción 2: Script Directo
```bash
python crear_audio.py
```

### Opción 3: Código Personalizado
```python
import pyttsx3

engine = pyttsx3.init()
engine.save_to_file("Tu texto aquí", "mi_audio.wav")
engine.runAndWait()
```

## 🎨 Formatos Soportados

### Imágenes de Entrada
- ✅ JPG/JPEG
- ✅ PNG
- ✅ BMP
- ✅ Resoluciones: 256x256 a 4K

### Audio de Entrada
- ✅ WAV (recomendado)
- ✅ MP3
- ✅ M4A
- ✅ AAC

### Video de Salida
- ✅ MP4 (defecto)
- ✅ AVI
- ✅ MOV

## ⚠️ Limitaciones Importantes

### Dependencias y Compatibilidad
Incluso si encontráramos el repositorio perfecto en GitHub para la animación de labios, nos enfrentaríamos al mismo problema: **no podríamos instalar las dependencias necesarias** (como OpenCV, PyTorch, ffmpeg, etc.) para que funcione.

Esta es la razón por la que este proyecto incluye:
- **Múltiples implementaciones** con diferentes niveles de dependencias
- **Versión ultra-simple** que solo usa PIL y pyttsx3
- **Fallbacks** para cuando las librerías complejas fallan
- **Entornos virtuales** pre-configurados para diferentes casos

### Por Qué Existen Estas Limitaciones
- 🔴 **OpenCV**: Problemas de compilación en algunos sistemas
- 🔴 **PyTorch**: Requiere versiones específicas de Python/CUDA
- 🔴 **MediaPipe**: No siempre compatible con todas las versiones
- 🔴 **FFmpeg**: Instalación externa requerida
- 🔴 **numba**: Conflictos con Python 3.14+

### Nuestra Solución
Este proyecto está diseñado para **funcionar a pesar de estas limitaciones**, ofreciendo alternativas que van desde básicas hasta avanzadas según lo que esté disponible en tu sistema.

## 🔧 Solución de Problemas

### Error: "No se detectó cara"
```bash
# Verifica que la imagen tenga una cara visible
# Prueba con diferentes imágenes
# Asegúrate de buena iluminación en la imagen
```

### Error: "FFmpeg no encontrado"
```bash
# Windows: Descargar desde https://ffmpeg.org/
# Agregar FFmpeg al PATH del sistema
# Verificar: ffmpeg -version
```

### Error: "Audio no encontrado"
```bash
# Verifica la ruta del archivo
# Crea audio con crear_audio.py
# Usa formatos soportados (WAV, MP3)
```

### Error: "numba no compatible"
```bash
# Este proyecto evita numba por compatibilidad
# Usa wav2lip_simple.py o wav2lip_mejorado.py
# Están optimizados para Python 3.14
```

## 📈 Optimización de Rendimiento

### Para Videos Largos
- Usa `wav2lip_simple.py` para velocidad
- Reduce resolución de imagen
- Corta audio a segmentos más cortos

### Para Máxima Calidad
- Usa `wav2lip_mejorado.py`
- Imagen de alta resolución (pero no más de 1080p)
- Audio claro y sin ruido de fondo

## 🎯 Consejos para Mejores Resultados

### Imagen Ideal
- 👤 Una sola persona visible
- 😊 Cara frontal o ligeramente ladeada
- 💡 Buena iluminación
- 📐 Resolución mínima 512x512

### Audio Ideal
- 🎙️ Voz clara y sin eco
- 🔊 Volumen consistente
- ⏱️ Duración 3-30 segundos (óptimo)
- 🎵 Formato WAV para mejor calidad

## 🚀 Extensiones Futuras

- [ ] Soporte para múltiples caras
- [ ] Integración con modelos de IA más avanzados
- [ ] Interface gráfica (GUI)
- [ ] Procesamiento en lotes
- [ ] Soporte para webcam en tiempo real

## 📝 Licencia

Este proyecto es educativo y combina:
- Código original de Wav2Lip (MIT License)
- Implementaciones propias (MIT License)
- Librerías de terceros (ver LICENSE de cada una)

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas!
1. Fork el proyecto
2. Crea tu feature branch
3. Commit tus cambios
4. Push al branch
5. Abre un Pull Request

## 📞 Soporte

Si encuentras problemas:
1. Revisa esta documentación
2. Verifica los requisitos
3. Ejecuta `wav2lip_suite.py` para diagnósticos
4. Usa la versión Simple como fallback

---

**¡Disfruta creando videos con sincronización de labios! 🎬✨**