import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from requests.exceptions import HTTPError
import re

x_parser = "html.parser"

def extract_paragraphs(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, x_parser)

        paragraphs = []
        for paragraph in soup.find_all('p'):
            text = paragraph.get_text().strip()
            if text:
                #print(text,"\n")
                paragraphs.append(text)

        combined_text = ' '.join(paragraphs)
        combined_text = re.sub(r'\n+', ' ', combined_text)
        return combined_text
    except requests.exceptions.RequestException as e:
        print('Error al extraer los párrafos:', e)
        return None
    
def get_sources(texto_pp):
    fuentes_confiables = ['marca.com', 'lavanguardia.com', 'elplural.com', 'elmundo.es', 'elespanol.com', 'bbc.com', 'heraldo.es', '20minutos.es', 'elpais.com', 'cnnespanol.cnn.com', 'eltiempo.com', 'semana.com', 'pulzo.com', 'elespectador.com', 'las2orillas.co', 'publimetro.co', 'cambiocolombia.com', 'elnuevosiglo.com.co', 'qhubo.com', 'extra.com.co', 'diarioadn.co', 'desdeabajo.info', 'confidencialcolombia.com', 'latitud435.com', 'eldeportivo.com.co', 'elperiodicodeportivo.com.co', 'portafolio.co', 'larepublica.co', 'elcolombiano.com', 'minuto30.com', 'elmundo.com', 'elpalpitar.com', 'elrionegrero.com', 'elheraldo.co', 'zonacero.com', 'aldia.co', 'diariolalibertad.com', 'hora724.com', 'eluniversal.com.co', 'mundonoticias.com.co', 'bolivarense.com', 'maganguehoy.co', 'periodicoeldiario.com', 'lapatria.com', 'eje21.com.co', 'elnuevoliberal.com', 'periodicovirtual.com', 'diariodelcauca.com.co', 'periodicolacampana.com', 'elpilon.com.co', 'diariodelcesar.com', 'elpaisvallenato.com', 'midiario.co', 'interpolitico.com', 'elmanduco.com.co', 'larazon.co', 'elmeridiano.co', 'lapiragua.co', 'tuprensadigital.com', 'eltelegrafo.co', 'diariosigloxxi.co', 'periodismopublico.com', 'lanacion.com.co', 'diariodelhuila.com', 'opanoticias.com', 'diariodelnorte.net', 'laguajirahoy.com', 'elpulsocaribe.com', 'guajiragrafica.net', 'periodicolaguajira.com', 'hoydiariodelmagdalena.com', 'elinformador.com.co', 'seguimiento.co', 'santamartaaldia.co', 'periodicodelmeta.com', 'llanosietedias.com', 'llanoalmundo.com', 'noticierodelllano.com', 'diariodelsur.com.co', 'nariñohoy.com', 'laopinion.com.co', 'asiescucuta.com', 'elquindiano.com', 'cronicadelquindio.com', '180grados.digital', 'eldiario.com.co', 'risaraldahoy.com', 'elexpreso.co', 'thearchipielagopress.com', 'vanguardia.com', 'elfrente.com.co', 'elmeridiano.co', 'sucrenoticias.com', 'portallavoz.com', 'elnuevodia.com.co', 'elolfato.com', 'alaluzpublica.com', 'periodicodehoy.com', 'elpais.com.co', 'qhubocali.com', 'occidente.co', 'soydebuenaventura.com']
    query = ' '.join(texto_pp) + ", noticia actual"
    url = "http://172.174.160.126:8080/search"
    data = []
    _id = 0
    saved_titles = []  # Lista auxiliar para almacenar los títulos guardados

    for pageno in range(1, 11):
        params = {
            "q": query,
            "categories": "general",
            "pageno": pageno,
        }
        response = requests.get(url, params=params)
        if not response.ok:
            raise HTTPError(f"Error al obtener fuentes, código HTTP: {response.status_code}")
        soup = BeautifulSoup(response.text, x_parser)
        articles = soup.find_all('article', {'class': 'result'})
        for article in articles:
            title = article.find('h3').text
            source = article.find('a', {'class': 'url_wrapper'}).get('href')
            description = article.find('p', {'class': 'content'}).text
            # Obtener el dominio de la fuente
            domain = urlparse(source).netloc.lstrip("www.")

            # Verificar si el título ya se encuentra en saved_titles
            if title in saved_titles:
                continue

            # Verificar si el dominio es una fuente confiable
            if domain in fuentes_confiables:
                if "-" in title:
                    posicion = title.find("-")
                    title = title[:posicion]
                elif "|" in title:
                    posicion = title.find("|")
                    title = title[:posicion]
                if "..." in title:
                    try:
                        posicion = title.find("...")
                        title_new = title[:posicion]  # Eliminar los tres puntos al final del título
                        # Realizar la solicitud de la página del artículo y obtener su contenido
                        article_response = requests.get(source)
                        article_content = article_response.content
                        article_soup = BeautifulSoup(article_content, x_parser)
                        texto_completo = ""
                        try:
                            texto_completo = article_soup.find('h1').text
                            if "access denied" in texto_completo.lower():
                                continue
                            elif texto_completo.split()[0] != title_new.split()[0]:
                                texto_completo = ""
                        except Exception:
                            pass
                        if texto_completo:
                            _id += 1
                            data.append({
                                '_id': _id,
                                'title': texto_completo.strip(),
                                'source': source,
                                'description': description.strip(),
                            })
                            saved_titles.append(title)  # Agregar el título a saved_titles
                        else:
                            # Buscar el texto de la página que comienza con el título del artículo
                            # Corregir funcionamiento
                            for element in article_soup.find_all(text=True):
                                if title_new.strip() in element.strip():
                                    # Si se encuentra el inicio del texto, se extrae el texto completo
                                    texto_completo = element.find_next_sibling(text=True)
                                    break
                            if texto_completo:
                                _id += 1
                                data.append({
                                    '_id': _id,
                                    'title': texto_completo.strip(),
                                    'source': source,
                                    'description': description.strip(),
                                })
                                saved_titles.append(title)  # Agregar el título a saved_titles

                    except Exception:
                        _id += 1
                        data.append({
                            '_id': _id,
                            'title': title.strip(),
                            'source': source,
                            'description': description.strip(),
                        })
                        saved_titles.append(title)  # Agregar el título a saved_titles
                else:
                    _id += 1
                    data.append({
                        '_id': _id,
                        'title': title.strip(),
                        'source': source,
                        'description': description.strip(),
                    })
                    saved_titles.append(title)  # Agregar el título a saved_titles

    return data
