from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json
from selenium.webdriver.common.keys import Keys
from argostranslate import package, translate
import re

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("debuggerAddress", "localhost:9222")
driver = webdriver.Chrome(options=chrome_options)

package.install_from_path('./utils/translate-en_es-1_0.argosmodel')
package.install_from_path('./utils/translate-es_en-1_0.argosmodel')

def get_argos_model(source, target):
    lang = f'{source} -> {target}'
    source_lang = [model for model in translate.get_installed_languages() if lang in map(repr, model.translations_from)]
    target_lang = [model for model in translate.get_installed_languages() if lang in map(repr, model.translations_to)]
    
    return source_lang[0].get_translation(target_lang[0])

argos_en_es = get_argos_model('English', 'Spanish')
argos_es_en = get_argos_model('Spanish', 'English')
ventanas = driver.window_handles

def obtener_respuesta(texto):
    driver.switch_to.window(ventanas[0])
    time.sleep(2)
    # Obtener la URL actual
    current_url = driver.current_url
    print("URL: ",current_url)
    # Verificar si la URL es "https://bard.google.com/"
    if current_url == "https://bard.google.com/?hl=en":
        # Encontrar el elemento de texto (textarea) mediante su identificador (id)
        text_area = driver.find_element(By.ID, "mat-input-0")
        # Escribir "prompt" en el elemento de texto
        text_area.send_keys(texto)
        # Encontrar el botón mediante una combinación de atributos
        time.sleep(3)
        button = driver.find_element(By.CSS_SELECTOR, 'button[mattooltip="Submit"]')
        # Hacer clic en el botón
        button.click()

        time.sleep(15)
        message_contents = driver.find_elements(By.TAG_NAME, "message-content")

        # Obtener el contenido del último elemento <message-content>
        if message_contents:
            last_message_content = message_contents[-1]
            #print("Mensaje:", last_message_content.text)
            return last_message_content.text

def translate_text(text, src):
    if src == "en":
        traducido = argos_en_es.translate(text)
        traducido = traducido.replace("\n\n","\n")
        traducido = traducido.strip()
        return traducido
    else:
        return argos_es_en.translate(text)

def verificar_llm(texto):
    texto = translate_text(texto, "es")
    prompt = "Check the following news: '" + texto + "'. Your answer should be: Only answer any of these possible answers: 'True', 'False', 'Partially true', 'Not enough information'."
    print(prompt)
    output = obtener_respuesta(prompt)
    return separar_respuesta(output)

def separar_respuesta(texto):
    respuestas = ["partially true", "true", "false", "not enough information"]
    respuesta_encontrada = None
    texto2 = texto.split(".")
    for respuesta in respuestas:
        if respuesta.lower() in texto2[0].lower():
            respuesta_encontrada = respuesta.lower()
            break

    if respuesta_encontrada:
        # Eliminar el fragmento anterior a la respuesta
        texto = texto.replace(texto[:texto.lower().index(respuesta_encontrada)], "")
        texto = texto.replace(respuesta_encontrada.capitalize() + ".", "", 1)
        print(texto)
        if(respuesta_encontrada == "true"):
            respuesta = "Verdadera"
        elif(respuesta_encontrada == "false"):
            respuesta = "Falsa"
        elif(respuesta_encontrada == "partially true"):
            respuesta = "Parcialmente verdadera"
        elif(respuesta_encontrada == "not enough information"):
            respuesta = "Sin información suficiente"
        else:
            respuesta = "Sin información suficiente"
        
        texto = translate_text(texto, "en")
        return respuesta, texto.strip()
    else:
        texto = translate_text(texto, "en")
        return None, texto.strip()


def analizar_con_llm(texto, fuente1, fuente2, ad_info):
    driver.switch_to.window(ventanas[1])
    time.sleep(2)
    print("URL: ", driver.current_url)
    # buscar <div class="flex flex-col w-full py-2 flex-grow md:py-3 md:pl-4 relative border border-black/10 bg-white dark:border-gray-900/50 dark:text-white dark:bg-gray-700 rounded-md shadow-[0_0_10px_rgba(0,0,0,0.10)] dark:shadow-[0_0_15px_rgba(0,0,0,0.10)]"><textarea id="prompt-textarea" tabindex="0" data-id="root" rows="1" placeholder="Send a message..." class="m-0 w-full resize-none border-0 bg-transparent p-0 pr-7 focus:ring-0 focus-visible:ring-0 dark:bg-transparent pl-2 md:pl-0" style="max-height: 200px; height: 24px; overflow-y: hidden;"></textarea><button disabled="" class="absolute p-1 rounded-md text-gray-500 bottom-1.5 md:bottom-2.5 hover:bg-gray-100 enabled:dark:hover:text-gray-400 dark:hover:bg-gray-900 disabled:hover:bg-transparent dark:disabled:hover:bg-transparent right-1 md:right-2 disabled:opacity-40"><svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4 mr-1" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><line x1="22" y1="2" x2="11" y2="13"></line><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon></svg></button></div> dar click
    input_box = driver.find_element(By.XPATH,'//*[@id="prompt-textarea"]')
    entrada = "Valida la siguiente noticia con la información que te voy a dar"
    time.sleep(1)
    input_box.send_keys(entrada)
    time.sleep(1)
    input_box.send_keys(Keys.SHIFT + Keys.ENTER)
    entrada = f"Noticia: {texto}"
    time.sleep(1)
    input_box.send_keys(entrada)
    time.sleep(1)
    input_box.send_keys(Keys.SHIFT + Keys.ENTER)
    entrada = f"Fuente 1: {fuente1}"
    time.sleep(1)
    input_box.send_keys(entrada)
    time.sleep(1)
    input_box.send_keys(Keys.SHIFT + Keys.ENTER)
    entrada = f"Fuente 2: {fuente2}"
    time.sleep(1)
    input_box.send_keys(entrada)
    time.sleep(1)
    input_box.send_keys(Keys.SHIFT + Keys.ENTER)
    entrada = f"Información adicional de peso y actualizada: {ad_info}"
    time.sleep(1)
    input_box.send_keys(entrada)
    input_box.send_keys(Keys.SHIFT + Keys.ENTER)
    entrada = "Tu respuesta debe ser en formato JSON y en un solo párrafo:"
    time.sleep(1)
    input_box.send_keys(entrada)
    time.sleep(1)
    input_box.send_keys(Keys.SHIFT + Keys.ENTER)
    entrada = "validacion: Verdadera, Falsa, Parcialmente verdadera, Sin información suficiente"
    time.sleep(1)
    input_box.send_keys(entrada)
    time.sleep(1)
    input_box.send_keys(Keys.SHIFT + Keys.ENTER)
    entrada = "razon: Incluye una razón por la cuál la noticia obtuvo esa 'Validación'"
    time.sleep(1)
    input_box.send_keys(entrada)
    time.sleep(1)
    input_box.send_keys(Keys.SHIFT + Keys.ENTER)
    input_box.send_keys(Keys.SHIFT + Keys.ENTER)
    entrada = "Nota: para que validación sea 'Sin información suficiente' es porque la noticia ingresada le faltan datos para poder comprarar con las fuentes, o porque las fuentes no tengan nada que ver con la noticia; si la noticia es afirmada pero dice textualmente que no ha sido comprobada o confirmada aún entonces queda es 'Parcialmente verdadera'"
    time.sleep(1)
    input_box.send_keys(entrada)
    time.sleep(1)
    input_box.send_keys(Keys.ENTER)
    time.sleep(5)

    # Mientras no aparezca <button class="btn relative btn-neutral border-0 md:border" as="button">...</button> no se continuará, esperar 2 segundos para cada siguiente búsqueda del botón
    while True:
        print("Esperando respuesta")
        try:
            button = driver.find_element(By.CSS_SELECTOR, 'button.btn-neutral div')
            if button.text == "Regenerate response":
                break
            else:
                time.sleep(2)
        except Exception:
            time.sleep(2)

    try:
        response_elements = driver.find_elements(By.XPATH, '//p')

        if response_elements:
            last_response_element = response_elements[-2]
            response_json = last_response_element.get_attribute('textContent')
            response_dict = json.loads(response_json)

            # Obtener los valores de "Validación" y "Razón"
            validacion = response_dict["validacion"]
            razon = response_dict["razon"]

            # Mostrar la respuesta
            respuesta = {
                "validacion": validacion,
                "razon": razon
            }
            return respuesta        
        else:
            print("No se encontraron respuestas.")
    except Exception:
        return "No se encontraron respuestas válidas"


def verificar(texto, fuente1, fuente2):
    ad_info = ""
    try:
        respuesta, ad_info = verificar_llm(texto)
        combined_text = str(respuesta) + re.sub(r'\n+', ' ', ad_info)
        return analizar_con_llm(texto, fuente1, fuente2, combined_text)
    except Exception:
        return None
    
    
