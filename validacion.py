from preprocesamiento import Tokenizar

def Validar(clf, real_vectorizer, frase: str):
    frase_X = real_vectorizer.transform([frase])
    prediccion = clf.predict(frase_X)
    probabilidad = clf.predict_proba(frase_X)
    return (frase, prediccion[0], [probabilidad[0][0],probabilidad[0][1]])
