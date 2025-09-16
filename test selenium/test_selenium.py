from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# CONFIGURAR EL SERVICIO DE CHROMEDRIVER EN MAC
servicio = Service(executable_path="/opt/homebrew/bin/chromedriver")
driver = webdriver.Chrome(service=servicio)

# ABRIR ARCHIVO HTML LOCAL EN EL NAVEGADOR
driver.get("file:///Users/moliimoli/Desktop/test%20selenium/selenium.html")

# DEFINIR TIEMPO DE ESPERA ENTRE ACCIONES O SECCIONES
espera = 7

# FUNCION PARA VALIDAR QUE UNA SECCION DEL MENU SE CARGUE CORRECTAMENTE
def validar_seccion(link_text, section_id):
    try:
        # HACER CLICK EN EL LINK DE LA SECCION
        driver.find_element(By.LINK_TEXT, link_text).click()
        # ESPERAR HASTA QUE EL ELEMENTO CON ID DE LA SECCION ESTÉ PRESENTE
        WebDriverWait(driver, espera).until(
            EC.presence_of_element_located((By.ID, section_id))
        )
        # IMPRIMIR MENSAJE DE CONFIRMACION DE CARGA CORRECTA
        print(f"✅ Sección '{link_text}' cargada correctamente")
        # PAUSA PARA VISUALIZAR LA SECCION
        time.sleep(espera)
    except Exception as e:
        # IMPRIMIR MENSAJE DE ERROR SI NO SE PUEDE CARGAR LA SECCION
        print(f"❌ ERROR: No se pudo cargar la sección '{link_text}' - {e}")

# === CASO DE PRUEBA 1: VALIDAR QUE LA PAGINA PRINCIPAL SE CARGUE ===
try:
    # ESPERAR HASTA QUE EL TITULO (TAG H1) ESTÉ PRESENTE
    WebDriverWait(driver, espera).until(
        EC.presence_of_element_located((By.TAG_NAME, "h1"))
    )
    # OBTENER EL TEXTO DEL TITULO
    titulo = driver.find_element(By.TAG_NAME, "h1").text
    # VERIFICAR QUE EL TITULO CONTENGA EL TEXTO ESPERADO
    assert "Restaurante Sabores de Chile" in titulo
    # IMPRIMIR MENSAJE DE EXITO
    print("✅ Página cargada correctamente")
    # PAUSA PARA VISUALIZAR
    time.sleep(espera)
except Exception as e:
    # IMPRIMIR MENSAJE DE ERROR SI LA PAGINA NO SE CARGA
    print(f"❌ ERROR: La página no se cargó correctamente - {e}")

# === VALIDAR TODAS LAS SECCIONES DEL MENU ===
secciones = [
    ("¿Quiénes somos?", "quienes-somos"),
    ("Platos Principales", "platos"),
    ("Bebestibles", "bebestibles"),
    ("Postres", "postres"),
    ("Especialidades", "especialidades"),
]

# RECORRER TODAS LAS SECCIONES Y VALIDAR CADA UNA
for link, section_id in secciones:
    validar_seccion(link, section_id)

# === FUNCION PARA VALIDAR VIDEO O IFRAME Y REDIRIGIR A YOUTUBE SI NO CARGA ===
def probar_video_y_redirigir():
    try:
        try:
            # INTENTAR LOCALIZAR UN VIDEO
            video = driver.find_element(By.TAG_NAME, "video")
        except:
            # SI NO HAY VIDEO, BUSCAR UN IFRAME
            video = driver.find_element(By.TAG_NAME, "iframe")
        
        # OBTENER LA FUENTE DEL VIDEO/IFRAME
        src = video.get_attribute("src")
        if src and "http" in src:
            # SI TIENE FUENTE VALIDA, IMPRIMIR CONFIRMACION
            print(f"✅ Video encontrado con fuente: {src}")
        else:
            # SI NO TIENE FUENTE VALIDA, REDIRIGIR A YOUTUBE
            print("❌ Video no tiene fuente válida. Redirigiendo a YouTube...")
            driver.get("https://youtu.be/lKXvRuivFwo?si=wckgjKbxbvQgEsaT")
    except Exception as e:
        # SI HAY CUALQUIER ERROR AL LOCALIZAR EL VIDEO, REDIRIGIR A YOUTUBE
        print(f"❌ ERROR: No se pudo localizar el video - {e}")
        driver.get("https://youtu.be/lKXvRuivFwo?si=wckgjKbxbvQgEsaT")

# EJECUTAR LA PRUEBA DEL VIDEO
probar_video_y_redirigir()
time.sleep(espera)

# === EVIDENCIA: TOMAR CAPTURA DE PANTALLA FINAL ===
driver.save_screenshot("evidencia_restaurante.png")
print("📸 Captura de pantalla guardada como 'evidencia_restaurante.png'")

# CERRAR NAVEGADOR AL FINAL DE LA PRUEBA
driver.quit()
