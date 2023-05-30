from flask import Flask, request, jsonify
import joblib
import spacy
from preprocesamiento import Tokenizar
from validacion import Validar
from flask_cors import CORS
from search_sources import get_sources
from match import similarity
import numpy as np
import requests
#from check_llm import verificar_llm (PROXIMAMENTE; MEJORA)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Cargar el modelo y el vectorizador
clf = joblib.load('./utils/clf.joblib')
real_vectorizer = joblib.load('./utils/real_vectorizer.joblib')

# Cargar el modelo de spaCy
nlp = spacy.load('es_dep_news_trf')

@app.route('/')
def welcome():
    return 'Welcome to the RealCheck API!'

# Definir la ruta para el endpoint de predicción
@app.route('/verificar', methods=['POST'])
def predict_sentiment():
    # Obtener el texto de entrada de la solicitud POST
    texto = request.get_json()['texto']
    # Restringir el uso del backend a solo nuestro frontend
    #if not request.referrer.startswith('http://172.190.53.35:3000'): 
    #    return jsonify({'error': 'Acceso denegado'})
    result = Validar(clf, real_vectorizer, texto)
    #print(result)
    return jsonify({'text': texto, 'verificabilidad': int(result[1]), 'probabilidad': result[2]})

# Definir la ruta para el endpoint de buscar las fuentes
@app.route('/search', methods=['POST'])
def search_sources():
    texto = request.get_json()['texto']
    texto_pp = Tokenizar(texto)
    # Restringir el uso del backend a solo nuestro frontend
    #if not request.referrer.startswith('http://172.190.53.35:3000'): 
    #    return jsonify({'error': 'Acceso denegado'})
    # Buscar las fuentes en searXNG
    result = get_sources(texto_pp)
    return jsonify({'preprocesado': texto_pp, 'sources': result})
    
@app.route('/check', methods=['POST'])
def check_similarity():
    #print("REQUEST_URL: ",request.url)
    texto = request.get_json()['texto']
    titulares = request.get_json()['titulares']
    #print("Texto: ",texto)
    #print("Titulares: ",titulares)
    # Restringir el uso del backend a solo nuestro frontend
    #if not request.referrer.startswith('http://172.190.53.35:3000'): 
    #    return jsonify({'error': 'Acceso denegado'})
    titulares_seleccionados, probabilidades = similarity(texto, titulares)
    probabilidades =  np.array(probabilidades, dtype=np.float32).tolist()
    return jsonify({'titulares_seleccionados': titulares_seleccionados, 'probabilidades': probabilidades})

@app.route('/check_llm', methods=['POST'])
def news_checker():
    texto = request.get_json()['texto']
    fuente1 = request.get_json()['fuente1']
    fuente2 = request.get_json()['fuente2']
    print("Texto: ",texto)
    # Restringir el uso del backend a solo nuestro frontend
    #if not request.referrer.startswith('http://172.190.53.35:3000'): 
    #    return jsonify({'error': 'Acceso denegado'})
    # Proximamente: Mejora de algoritmo de verificación con LLM
    #res , reason = verificar_llm(texto)
    #return jsonify({'res': res, 'reason': reason})
    # Definir la URL del endpoint al que deseas hacer la petición
    url = 'http://52.188.17.107:5000/analizar_llm'
    # Crear los datos en formato JSON que se enviarán en la solicitud POST
    data = {
        'texto': texto,
        'fuente1': fuente1,
        'fuente2': fuente2
    }
    # Realizar la solicitud POST al endpoint
    response = requests.post(url, json=data)
    return response

# Obtener la respuesta en formato JSON

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, use_reloader=True) 
