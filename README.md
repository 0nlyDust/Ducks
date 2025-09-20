# 🌸 Estanque de Patitos 🌸

¡Bienvenido al **Estanque de Patitos**! 🦆💖
Un juego relajante donde cuidas patitos en un estanque animado. Añade patitos, despiértalos si están dormidos y recoge corazones para ganar puntos.

---

## 🎮 Cómo jugar

* **Añadir patitos:** Clic sobre el estanque.
* **Despertar patitos dormidos:** Clic sobre un pato dormido.
* **Recoger corazones:** Clic en los corazones para sumar puntos.
* **Tienda:** Compra accesorios y equipa a tus patitos.

---

## 🦆 Mecánicas del juego

* Máximo **10 patitos** simultáneos.
* Los patitos pueden **dormirse** o **salir volando**.
* Personaliza tus patitos con accesorios de la **tienda**.
* Música de fondo y efectos de sonido agradables.

---

## ⚙️ Ejecutar desde el código fuente

### Requisitos

* Python 3.11 o superior
* Librerías: `pygame`, `Pillow`

```bash
pip install pygame pillow
```

### Generar el ejecutable (.exe) con PyInstaller

1. Instala PyInstaller:

```bash
pip install pyinstaller
```

2. Desde la carpeta que contiene `juego_patitos.py`, ejecuta:

```bash
pyinstaller --onefile --windowed juego_patitos.py
```

* `--onefile` → genera un único `.exe`
* `--windowed` → evita que se abra la consola junto al juego

3. El `.exe` se crea en la carpeta `dist/`.
4. Copia también las carpetas `imagenes` y `sonidos` junto al `.exe` si no las empaquetas dentro.

¡Diviértete cuidando a tus patitos! 🌸🦆💖
