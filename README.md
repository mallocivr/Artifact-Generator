# Malloci Artifact Generator

Backend code to generate artifacts from text. Access via an API endpoint. Currently running on Flask.

## Dependencies
- Python 3.6
- Flask, Flask-Cors
```
pip install Flask
pip install flask-cors
```
- Spacy
```
pip install spacy
python -m spacy download en_core_web_sm
```
- [Phrasemachine](https://github.com/slanglab/phrasemachine)
```
pip install phrasemachine
```

## Endpoints
`POST /generate` generate artifacts  

**Input JSON**
POST body [example in this gist.](https://gist.github.com/MGutensohn/8bc8b3ad144674fcf6b415a8dfb8f4ab)

**Return JSON**
The returned JSON will have an additional `artifacts` field added to every `room` and `subroom` passed in input.

## Usage

Start app
```
python app.py 
```

Generate artifacts
```
curl -X POST -H "Content-Type: application/json" -d @proposal.json http://127.0.0.1:5000/generate
```