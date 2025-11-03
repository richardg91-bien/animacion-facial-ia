# 🐳 WAV2LIP con Docker - Guía Completa

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
docker run --rm \
  -v "$(pwd)/input:/app/input" \
  -v "$(pwd)/resultados:/app/resultados" \
  wav2lip-app \
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
