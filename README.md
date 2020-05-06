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
-scikit-learn
```
pip install scikit-learn
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
python main.py 
```

Generate artifacts
```
curl -X POST -H "Content-Type: application/json" -d @proposal.json http://127.0.0.1:5000/generate
```


## Local Endpoint

```
curl -X POST -H "Content-Type: application/json" -d @proposal.json http://127.0.0.1:8080/generate
```

## Deplying to google cloud
```
gcloud app deploy
```

## Google Cloud Endpoint
```
curl -X POST -H "Content-Type: application/json" -d @test.json https://malloci.uc.r.appspot.com/generate > test.result.json
```

curl -X POST -H "Content-Type: application/json" -d @test.json http://127.0.0.1:8080/generate