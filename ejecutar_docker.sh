#!/bin/bash
echo "🐳 Ejecutando WAV2LIP en Docker..."

# Crear directorios necesarios
mkdir -p input
mkdir -p resultados

# Construir imagen Docker
docker build -t wav2lip-app .

# Ejecutar en modo test
docker run --rm -v "$(pwd)/resultados:/app/resultados" wav2lip-app python wav2lip_cli.py --test

echo "✅ Proceso completado. Revisa la carpeta 'resultados'"
