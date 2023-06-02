from flask import Flask, request, jsonify
import joblib
import spacy
from preprocesamiento import Tokenizar
from validacion import validar
from flask_cors import CORS
from search_sources import get_sources, extract_paragraphs
from match import similarity
import numpy as np
import requests
#from check_llm import verificar_llm (PROXIMAMENTE: MEJORA)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CSRF_ENABLED'] = False

# Cargar el modelo y el vectorizador
clf = joblib.load('./utils/clf.joblib')
real_vectorizer = joblib.load('./utils/real_vectorizer.joblib')

# Cargar el modelo de spaCy
nlp = spacy.load('es_dep_news_trf')
msg_den = "Acceso denegado"
frontend = 'http://172.174.160.126:3000'

@app.route('/')
def welcome():
    return 'Welcome to the RealCheck API!'

# Definir la ruta para el endpoint de predicción
@app.route('/verificar', methods=['POST'])
def predict_sentiment():
    # Obtener el texto de entrada de la solicitud POST
    texto = request.get_json()['texto']
    # Restringir el uso del backend a solo nuestro frontend
    if not request.referrer.startswith(frontend): 
        return jsonify({'error': msg_den})
    result = validar(clf, real_vectorizer, texto)
    return jsonify({'text': texto, 'verificabilidad': int(result[1]), 'probabilidad': result[2]})

# Definir la ruta para el endpoint de buscar las fuentes
@app.route('/search', methods=['POST'])
def search_sources():
    texto = request.get_json()['texto']
    texto_pp = Tokenizar(texto)
    # Restringir el uso del backend a solo nuestro frontend
    if not request.referrer.startswith(frontend): 
        return jsonify({'error': msg_den})
    # Buscar las fuentes en searXNG
    result = get_sources(texto_pp)
    return jsonify({'preprocesado': texto_pp, 'sources': result})
    
@app.route('/check', methods=['POST'])
def check_similarity():
    texto = request.get_json()['texto']
    titulares = request.get_json()['titulares']
    # Restringir el uso del backend a solo nuestro frontend
    if not request.referrer.startswith(frontend): 
        return jsonify({'error': msg_den})
    titulares_seleccionados, probabilidades = similarity(texto, titulares)
    probabilidades =  np.array(probabilidades, dtype=np.float32).tolist()
    return jsonify({'titulares_seleccionados': titulares_seleccionados, 'probabilidades': probabilidades})

@app.route('/check_llm', methods=['POST'])
def news_checker():
    texto = request.get_json()['texto']
    fuentes = request.get_json()['fuentes_escogidas']
    descrips = []
    for f in fuentes:
        descrips.append(extract_paragraphs(f["source"]))
    fuente1 = descrips[0]
    fuente2 = descrips[1]
    
    # Restringir el uso del backend a solo nuestro frontend
    if not request.referrer.startswith(frontend): 
        return jsonify({'error': msg_den})
    # Proximamente: Mejora de algoritmo de verificación con LLM
    try:
        # Validación con LLM
        url = 'http://172.174.160.126:7000/analizar_llm'
        data = {
            'texto': texto,
            'fuente1': fuente1,
            'fuente2': fuente2
        }
        response = requests.post(url, json=data)
        res = response.json()
        print(res)
        return jsonify({'res': res['validacion'], 'reason': res['razon'], 'fuentes': fuentes})
    except Exception:
        return jsonify({'res': 'No se puede validar con LLM en este momento', 'reason': 'No se pudo hacer la consulta desde el servidor, intente más tarde o contacte con un administrador', 'fuentes': fuentes})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, use_reloader=True) 
