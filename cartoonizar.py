import cv2
import numpy as np

def cartoonify_image(img_path):
    # Leer la imagen
    img = cv2.imread(img_path)
    if img is None:
        print(f"Error: No se pudo cargar la imagen en {img_path}")
        return

    # 1. Convertir a escala de grises
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 2. Desenfoque mediano para suavizar
    gray = cv2.medianBlur(gray, 5)

    # 3. Detección de bordes (líneas tipo dibujo)
    edges = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY,
        9, 9
    )

    # 4. Filtro bilateral (suaviza colores sin borrar bordes)
    color = cv2.bilateralFilter(img, 9, 250, 250)

    # 5. Combinar colores suavizados + bordes
    cartoon = cv2.bitwise_and(color, color, mask=edges)

    # Mostrar resultados
    cv2.imshow("Original", img)
    cv2.imshow("Cartoon", cartoon)
    cv2.imwrite("imagen_cartoonizada.jpg", cartoon)
    print("✅ Imagen cartoonizada guardada como 'imagen_cartoonizada.jpg'")

    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Usa tu propia imagen
imagen_de_entrada = 'woman-3584435_1280.jpg'
cartoonify_image(imagen_de_entrada)
