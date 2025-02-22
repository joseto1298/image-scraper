import os
import re
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import random
import json
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException

# Configuración de opciones para Chrome
options = Options()
options.binary_location = "/usr/bin/google-chrome"  # O la ruta correcta
options.headless = False
options.add_argument("--start-maximized")

# Especifica la ubicación del binario de Google Chrome o Chromium en Debian
options.binary_location = "/usr/bin/google-chrome-stable"  # Si instalaste Chromium
# options.binary_location = "/usr/bin/google-chrome"  # Si instalaste Google Chrome

# Configuración del servicio de ChromeDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Establecer el zoom al 25%
# driver.execute_script("document.body.style.zoom='25%'")


# Cargar cookies desde el archivo
def load_cookies(driver, cookies_file):
    if os.path.exists(cookies_file):
        with open(cookies_file, "r") as file:
            cookies = json.load(file)
            for cookie in cookies:
                if "sameSite" in cookie:
                    if cookie["sameSite"].lower() not in ["strict", "lax", "none"]:
                        del cookie["sameSite"]
                    else:
                        cookie["sameSite"] = cookie["sameSite"].capitalize()
                driver.add_cookie(cookie)
        print("Cookies cargadas desde el archivo.")

# Función para desplazarse hasta el final de la página
def scroll_to_bottom():
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        # Desplazamos hacia abajo hasta el final
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)  # Espera para permitir que la página cargue el contenido adicional

        # Esperamos que se cargue un nuevo elemento, si es necesario
        try:
            # Esperamos a que un nuevo bloque de imágenes o contenido esté visible
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.infinite-scroll-component__outerdiv"))
            )
        except:
            print("Tiempo de espera agotado o no se encontró el contenedor de scroll.")
            break

        # Verificamos la nueva altura
        new_height = driver.execute_script("return document.body.scrollHeight")

        # Si la altura no cambia, significa que hemos llegado al final
        if new_height == last_height:
            print("Se ha llegado al final de la página.")
            break

        last_height = new_height  # Actualizamos la última altura

# Función para simular la tecla de flecha derecha
def simulate_right_arrow_key():
    body = driver.find_element(By.TAG_NAME, "body")
    body.send_keys(Keys.RIGHT)
    time.sleep(2)

# Función para obtener seed, modelo, y otros datos
def get_metadata(driver):
    seed = model = created = owner = prompt_guidance = sampler = initial_image_strength = ""
    tags_removed = tags_prompt = []
    try:
        ul_elements = driver.find_element(By.CSS_SELECTOR, "ul.list-none.grid.grid-cols-2.gap-y-4.gap-x-2")
        elements = ul_elements.find_elements(By.CSS_SELECTOR, ".text-gray-200")
        try:
            seed = elements[0].text.strip()
        except (IndexError, NoSuchElementException) as e:
            print(f"Error al obtener seed: {e}")

        try:
            prompt_guidance = elements[1].text.strip()
        except (IndexError, NoSuchElementException) as e:
            print(f"Error al obtener prompt_guidance: {e}")

        try:
            sampler = elements[2].text.strip()
        except (IndexError, NoSuchElementException) as e:
            print(f"Error al obtener sampler: {e}")

        try:
            model = elements[3].text.strip()
        except (IndexError, NoSuchElementException) as e:
            print(f"Error al obtener model: {e}")
            
        try:
            created = elements[4].text.strip()
        except (IndexError, NoSuchElementException) as e:
            print(f"Error al obtener created: {e}")

        try:
            initial_image_strength = elements[5].text.strip()
        except (IndexError, NoSuchElementException) as e:
            print(f"Error al obtener prompt_guidance: {e}")
            
        try:
            owner_elements = driver.find_elements(By.CSS_SELECTOR, "span.color-white.text-base.textba")
            owner = owner_elements[1].text.strip()
        except (IndexError, NoSuchElementException) as e:
            print(f"Error al obtener owner: {e}")
        
        try:
            div_elements = driver.find_elements(By.CSS_SELECTOR, "div.mr-0")
            first_div = div_elements[0]
            paragraphs = first_div.find_elements(By.TAG_NAME, "p")
            tags_prompt = [re.sub(r"[(),]", "", p.text.strip()) for p in paragraphs]
        except (IndexError, NoSuchElementException) as e:
            print(f"Error al obtener tags_prompt: {e}")
        
        try:
            second_div = div_elements[1]
            paragraphs = second_div.find_elements(By.TAG_NAME, "p")
            tags_removed = [re.sub(r"[(),]", "", p.text.strip()) for p in paragraphs]
        except (IndexError, NoSuchElementException) as e:
            print(f"Error al obtener tags_removed: {e}")
        
    except (NoSuchElementException, IndexError) as e:
        print(f"Error al obtener metadatos: {e}")
    return seed, model, created, tags_removed, tags_prompt, owner, prompt_guidance, sampler, initial_image_strength

# Función para obtener la URL de "Inspired from"
def get_inspired_from(driver):
    try:
        # Dentro de ese div, buscar el enlace que contiene la imagen
        a_element = driver.find_element(By.CSS_SELECTOR, "a.playground-button")
        
        # Buscar la imagen dentro del enlace
        img_element = a_element.find_element(By.TAG_NAME, "img")
        
        # Obtener el atributo 'src' de la imagen
        img_src = img_element.get_attribute("src")
        
        return img_src
        
    except NoSuchElementException:
        print("Error al obtener 'Inspired from' o la imagen. No se encontró el elemento.")
        return ""

# Función para descargar y guardar la imagen
def download_image(img_url, img_filename):
    try:
        img_data = requests.get(img_url).content
        with open(img_filename, "wb") as file:
            file.write(img_data)
        print(f"Imagen descargada: {img_filename}")
    except Exception as e:
        print(f"Error al descargar la imagen: {e}")
        img_filename = "Error al descargar imagen"
    return img_filename

def store_image_error(image_count, url_actual):
    error_data = {
        "image_count": image_count,
        "error_url": url_actual,
    }
    
    if not os.path.exists("error_log.json"):
        with open("error_log.json", "w") as file:
            json.dump([], file)

    with open("error_log.json", "r+", encoding="utf-8") as file:
        try:
            existing_errors = json.load(file)
        except json.JSONDecodeError:
            existing_errors = []
        existing_errors.append(error_data)
        file.seek(0)
        json.dump(existing_errors, file, ensure_ascii=False, indent=4)
        file.truncate()
        print("Error registrado.")

def write_count_image(value, file_path="image_count.json"):
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump({"value": value}, file, ensure_ascii=False, indent=4)

def read_count_image(file_path="image_count.json"):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data.get("value")
    return 0

def store_image_data(img_url, img_filename, alt_text, seed, model, created, inspired_from, tags_removed, tags_prompt , owner, prompt_guidance, sampler, initial_image_strength):
    
    file = "image_data_Pepe2.json"
    
    image_data = {
        "image_url": img_url,
        "image_filename": img_filename,
        "prompt": alt_text,
        "seed": seed,
        "model": model,
        "created": created,
        "prompt_guidance": prompt_guidance,
        "sampler": sampler,
        "initial_image_strength": initial_image_strength,
        "owner": owner,
        "inspired_from": inspired_from,
        "tags_prompt": tags_prompt,
        "tags_removed": tags_removed
    }

    if not os.path.exists(file):
        with open(file, "w") as file:
            json.dump({}, file)

    with open(file, "r+", encoding="utf-8") as file:
        try:
            existing_data = json.load(file)
        except json.JSONDecodeError:
            existing_data = {}
        existing_data.update({img_url: image_data})
        file.seek(0)
        json.dump(existing_data, file, ensure_ascii=False, indent=4)
        file.truncate()
        print("Datos guardados.")
        
def search_image(driver):
    global image_count, downloaded_urls
        
    scroll_to_bottom()

    try:
        div_element = driver.find_element(By.CSS_SELECTOR, "div.infinite-scroll-component__outerdiv")
        img_elements = div_element.find_elements(By.TAG_NAME, "img")
                    
        print(f"Se encontraron {len(img_elements)} elementos img en la página.")
        
        if not img_elements:
            print("No se encontro imagen.")
        else:    
            for img in img_elements:
                try:
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", img)
                    time.sleep(0.5)

                    driver.execute_script("arguments[0].click();", img)
                    time.sleep(1)
                    
                    img_element = driver.find_element(By.CSS_SELECTOR, 'img[data-testid="image-post-image"]')

                    img_url = img_element.get_attribute("src")
                    alt_text = img_element.get_attribute("alt")
                    
                    if img_url != "URL no disponible" and img_url not in downloaded_urls:
                        
                        img_filename = os.path.join(image_folder, f"image_{image_count}.jpg")
                        download_image(img_url, img_filename)
                                                                        
                        seed, model, created, tags_removed, tags_prompt, owner, prompt_guidance, sampler, initial_image_strength  = get_metadata(driver)
                        inspired_from = get_inspired_from(driver)
                        store_image_data(img_url, img_filename, alt_text, seed, model, created, inspired_from, tags_removed, tags_prompt, owner,prompt_guidance, sampler, initial_image_strength)
                        
                        downloaded_urls.add(img_url)
                        
                except ElementClickInterceptedException:
                    print(f"Error al hacer clic en la imagen: {img_url}")
                    current_url = driver.current_url
                    store_image_error(image_count, current_url)
            
                time.sleep(1)
                driver.back()
                image_count += 1
                write_count_image(image_count)


    except TimeoutException:
        print("Error: No se pudo encontrar el elemento 'infinite-scroll-component__outerdiv' dentro del tiempo de espera.")
        
    # Preguntar al usuario si desea continuar
    user_input = input("¿Desea continuar? (s/n): ")
    if user_input.lower() == 's':
        search_image(driver)


# Variables globales
image_count = read_count_image()
downloaded_urls = set()

# URL de destino
url = "https://playground.com/profile/"

# Cargar una página inicial para poder cargar las cookies
driver.get("https://playground.com")

load_cookies(driver, "cookiesPepe2.json")

driver.get(url)

# Crear una carpeta para guardar imágenes
image_folder = "Pepe2"

if not os.path.exists(image_folder):
    os.makedirs(image_folder)

# Esperar a que el usuario interactúe manualmente
input("Presiona Enter para continuar después de interactuar manualmente...")


search_image(driver)

driver.quit()
exit()