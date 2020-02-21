# Malloci Artifact Generator

Flask API generate artifacts from text

## Dependencies
- Flask
- Python 3.6

## Endpoints



## Usage

Start app
```
python app.py 
```

Generate artifacts
```
curl -X POST -H "Content-Type: application/json" -d @proposal.json http://127.0.0.1:5000/parse
```