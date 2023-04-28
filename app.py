from flask import Flask, request, jsonify
import joblib
import spacy
from preprocesamiento import Tokenizar
from validacion import Validar
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["172.190.53.35"])

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
    result = Validar(clf, real_vectorizer, texto)
    print(result)
    return jsonify({'text': texto, 'verificabilidad': int(result[1]), 'probabilidad': result[2]})
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, use_reloader=False)
