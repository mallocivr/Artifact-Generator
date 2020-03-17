from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from generators import get_room_artifacts

app = Flask(__name__)
cors = CORS(app)


#############################################################
# API
#############################################################

@app.route("/")
def api_root():
  return "Malloci Artifact Generator"

#############################################################
# POST /generate
# 	Returns links of all images uploaded with this service
#############################################################
@app.route("/generate",  methods=['POST'])
def parse_doc():
	content = request.json
	
	for room in content['rooms']:
		room['parsed_artifacts'] = get_room_artifacts(room['text'])
		if 'subRooms' in room:
			for subroom in room['subRooms']:
				subroom['parsed_artifacts'] = get_room_artifacts(subroom['text'])

	return jsonify(content), 200


if __name__ == '__main__':
	app.run()