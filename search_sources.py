import requests
from bs4 import BeautifulSoup

def get_sources(texto_pp):
    query = ' '.join(texto_pp)
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

