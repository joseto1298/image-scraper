# Image Scraper

Este es un script en Python que utiliza Selenium para extraer imágenes de una página web, junto con sus metadatos, y las guarda en una carpeta local.

## Características
- Descarga imágenes automáticamente desde un sitio web.
- Extrae metadatos como la semilla, modelo, fecha de creación, propietario, etc.
- Utiliza cookies almacenadas para autenticarse.
- Realiza desplazamiento automático para cargar más imágenes.

## Requisitos
Asegúrate de tener instalados los siguientes paquetes:

```bash
pip install selenium requests webdriver-manager
```

Además, necesitas tener **Google Chrome** instalado y su versión compatible de **ChromeDriver**.

## Instalación
1. Clona este repositorio:

```bash
git clone https://github.com/TuUsuario/image_scraper.git
cd image_scraper
```

2. Instala las dependencias:

```bash
pip install -r requirements.txt
```

3. Guarda las cookies en `cookiesPepe2.json` si es necesario.

## Uso
Ejecuta el script con:

```bash
python scraper.py
```

El script descargará las imágenes y sus metadatos en la carpeta `Pepe2/`.

## Configuración Adicional
- Puedes modificar la carpeta de descarga en la variable `image_folder` dentro del código.
- Si necesitas más imágenes, ajusta el comportamiento del desplazamiento en `scroll_to_bottom()`.

## Contribución
Si deseas contribuir, siéntete libre de hacer un fork del repositorio y enviar un pull request con mejoras.

## Licencia
Este proyecto está bajo la licencia MIT.

