from flask import Flask, request, jsonify
from flask_cors import CORS
from gpt_scrap import verificar

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CSRF_ENABLED'] = False

@app.route('/')
def welcome():
    return 'Welcome to the RealCheck API_LLM!'

@app.route('/analizar_llm', methods=['POST'])
def analizar():
    texto = request.get_json()['texto']
    fuente1 = request.get_json()['fuente1']
    fuente2 = request.get_json()['fuente2']
    return jsonify(verificar(texto, fuente1, fuente2))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7000, debug=True, use_reloader=True) 