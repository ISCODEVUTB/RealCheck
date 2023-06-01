import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re

def extract_paragraphs(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

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
    url = "http://172.190.53.35:8080/search"
    data = []
    id = 0
    for pageno in range(1, 11):
        params = {
            "q": query,
            "categories": "general",
            "pageno": pageno,
        }
        response = requests.get(url, params=params)
        if not response.ok:
            raise Exception(f"Error al obtener fuentes, código HTTP: {response.status_code}")
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.find_all('article', {'class': 'result'})
        for article in articles:
            title = article.find('h3').text
            source = article.find('a', {'class': 'url_wrapper'}).get('href')
            description = article.find('p', {'class': 'content'}).text
            # Obtener el dominio de la fuente
            domain = urlparse(source).netloc.lstrip("www.")
            #print(domain, "-> ", domain in fuentes_confiables)
            if domain in fuentes_confiables:
                #print(title)
                if "-" in title:
                    posicion = title.find("-")
                    title = title[:posicion]
                elif "|" in title:
                    posicion = title.find("|")
                    title = title[:posicion]
                if "..." in title:
                    try:
                        posicion = title.find("...")
                        title_new = title[:posicion] # Eliminar los tres puntos al final del título
                        # Realizar la solicitud de la página del artículo y obtener su contenido
                        article_response = requests.get(source)
                        article_content = article_response.content
                        article_soup = BeautifulSoup(article_content, 'html.parser')
                        texto_completo = ""
                        try:
                            texto_completo = article_soup.find('h1').text
                            if "access denied" in texto_completo.lower():
                                continue
                            elif texto_completo.split()[0] != title_new.split()[0]:
                                texto_completo = ""
                        except:
                            pass
                        if texto_completo:
                            id += 1
                            data.append({
                                '_id': id,
                                'title': texto_completo.strip(),
                                'source': source,
                                'description': description.strip(),
                            })
                        else:
                            # Buscar el texto de la página que comienza con el título del artículo
                            # Corregir funcionamiento 
                            for element in article_soup.find_all(text=True):
                                #print(element, "-", title_new)
                                if title_new.strip() in element.strip():
                                    # Si se encuentra el inicio del texto, se extrae el texto completo
                                    texto_completo = element.find_next_sibling(text=True)
                                    #print("Nuevo texto: "+texto_completo)
                                    break
                            if texto_completo:
                                id += 1
                                data.append({
                                    '_id': id,
                                    'title': texto_completo.strip(),
                                    'source': source,
                                    'description': description.strip(),
                                })                       

                    except:
                        id += 1
                        data.append({
                            '_id': id,
                            'title': title.strip(),
                            'source': source,
                            'description': description.strip(),
                        })
                else:
                    id += 1
                    data.append({
                        '_id': id,
                        'title': title.strip(),
                        'source': source,
                        'description': description.strip(),
                    })

    return data