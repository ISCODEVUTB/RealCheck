import requests
from bs4 import BeautifulSoup

def get_sources(texto_pp):
    query = ' '.join(texto_pp)
    url = "http://172.190.53.35:8080/search"
    data = []
    id = 0
    for pageno in range(1, 2): #cambiar a 11
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
            id += 1
            data.append({
                '_id': id,
                'title': title,
                'source': source,
                'description': description.strip(),
            })

    return data

