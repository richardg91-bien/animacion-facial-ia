@echo off
echo 🐳 Ejecutando WAV2LIP en Docker...

REM Crear directorios necesarios
if not exist "input" mkdir input
if not exist "resultados" mkdir resultados

REM Construir imagen Docker
docker build -t wav2lip-app .

REM Ejecutar en modo test
docker run --rm -v "%cd%\resultados:/app/resultados" wav2lip-app python wav2lip_cli.py --test

echo ✅ Proceso completado. Revisa la carpeta 'resultados'
pause
