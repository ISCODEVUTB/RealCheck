# Prueba de ejecución con la librería spaCy

import spacy
import es_dep_news_trf

nlp = es_dep_news_trf.load()
doc = nlp("Esto es una frase.")

print([(w.text, w.pos_) for w in doc])