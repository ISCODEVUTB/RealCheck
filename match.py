from sklearn.metrics.pairwise import cosine_similarity
import fasttext

def similarity(text, titulares):
    # Cargar el modelo pre-entrenado de FastText en español
    modelo_ft = fasttext.load_model('cc.es.300.bin')
    
    # Procesar la frase y los titulares con FastText
    frase_vec = modelo_ft.get_sentence_vector(text)

    titulares_prob = []
    for titular in titulares:
        titular_vec = modelo_ft.get_sentence_vector(titular)
        prob = cosine_similarity(frase_vec.reshape(1, -1), titular_vec.reshape(1, -1))[0][0]
        titulares_prob.append((titular, prob))

    # Seleccionar los titulares con las 2 probabilidades más altas
    titulares_prob.sort(key=lambda x: x[1], reverse=True)
    titulares_prob = titulares_prob[1:3]

    # Guardar los titulares seleccionados y sus probabilidades en listas
    titulares_seleccionados = []
    probabilidades = []
    for i, (titular, prob) in enumerate(titulares_prob):
        titulares_seleccionados.append(titular)
        probabilidades.append(prob)

    # Cerrar el modelo
    del modelo_ft

    # Retornar las listas de titulares seleccionados y sus probabilidades
    return titulares_seleccionados, probabilidades