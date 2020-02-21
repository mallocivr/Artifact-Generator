# Malloci Artifact Generator

Backend code to generate artifacts from text. Access via an API endpoint. Currently running on Flask.

## Dependencies
- Flask
- Python 3.6

## Endpoints
- generate artifacts `POST /generate` 
**Input JSON**
```
{
    "name": "Exhibit Name",
    "rooms": [
        {
            "name": "Room 1",
            "subRooms": [],
            "text": "## Room 1 ..."
        },
        {
            "name": "Room 2",
            "subRooms": [],
            "text": "## Room 2 Text ..."
        },
        ...
    ],
    "text": "..."
}

```

**Return JSON**
```
{
    "name": "Exhibit Name",
    "rooms": [
        {
            "name": "Room 1",
            "subRooms": [],
            "text": "## Room 1 ...",
            "artifacts": [
            	{'type':'image', 'url':'http://image.png'},
            	{'type':'text', 'text':'.. artifact text...'},
            ]
        },
        {
            "name": "Room 2",
            "subRooms": [],
            "text": "## Room 2 Text ...",
            "artifacts": [
            	{'type':'image', 'url':'http://image2.png'},
            	{'type':'text', 'text':'.. artifact text...'},
            ]
        },
        ...
    ],
    "text": "..."
}

```

## Usage

Start app
```
python app.py 
```

Generate artifacts
```
curl -X POST -H "Content-Type: application/json" -d @proposal.json http://127.0.0.1:5000/generate
```