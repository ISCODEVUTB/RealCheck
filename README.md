
# RealCheck

Este proyecto es un verificador de noticias que utiliza inteligencia artificial para analizar y clasificar noticias como verdaderas o falsas. Está diseñado para ayudar a las personas a verificar la veracidad de las noticias que leen en línea y prevenir la propagación de información falsa. 

This project is a news checker that uses artificial intelligence to analyze and classify news as true or false. It is designed to help people verify the truth of the news they read online and prevent the spread of false information.

## Instalación

Clonar el repositorio usando `git`

```bash
  git clone https://github.com/NivekTar/realcheck.git
```

Acceder a la carpeta

```bash
  cd realcheck
  cd src
```

Crear un entorno virtual

```bash
  python3 -m venv venv
```

Acceder al entorno virtual
- Windows
```bash
  venv\Scripts\activate.bat
```
- Linux
```bash
  source venv/bin/activate
```

Instalar las librerias necesarias para funcionar, se instalará también el modelo pre-entrenado de **spaCy** llamado `es_dep_news_trf`.
```bash
  pip install -r requirements.txt
```

## Agradecimientos

 - [spaCy](https://spacy.io/) - Librería de procesamiento de lenguaje natural.
- Agradecemos al profesor [@EdwinPuertas](https://github.com/EdwinPuertas) por su guía en el desarrollo de este proyecto. 

## Autores

- [@NivekTar](https://github.com/NivekTar)
- [@sahirf](https://github.com/sahirf)
- [@anpiz](https://github.com/anpiz)

