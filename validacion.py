from preprocesamiento import tokenizar

def validar(clf, real_vectorizer, frase: str):
    frase_x = real_vectorizer.transform([frase])
    prediccion = clf.predict(frase_x)
    probabilidad = clf.predict_proba(frase_x)
    return (frase, prediccion[0], [probabilidad[0][0],probabilidad[0][1]])
