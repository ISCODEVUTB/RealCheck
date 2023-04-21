import es_dep_news_trf

nlp = es_dep_news_trf.load()

def Tokenizar(text: str):
    tokens = [token.lemma_.lower() for token in nlp(text) if not token.is_stop and not token.is_punct]
    return tokens