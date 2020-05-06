from flask import Flask, request, jsonify, Response
from flask_cors import CORS, cross_origin
from generators import get_room_artifacts

app = Flask(__name__)
# cors = CORS(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})



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
@cross_origin(origin="*", headers=['Content-Type','Authorization'])
def parse_doc():
	content = request.json
	
	for room in content['rooms']:
		room['artifacts'] = get_room_artifacts(room['text'])
		if 'subRooms' in room:
			for subroom in room['subRooms']:
				subroom['artifacts'] = get_room_artifacts(subroom['text'])

	css = ("<style>" 
	+ ".bold{font-weight:bold};" 
	+ ".italic{font-style:italic};" 
	+ ".emphasize{font-size:150%};" 
	+ "</style>")
	content['css'] = css

	return jsonify(content), 200
	# resp = Response(content, mimetype='application/json')
	# resp.headers['Access-Control-Allow-Origin'] = '*'
	# return resp


@app.route("/test", methods=['POST'])
def test():
	content = request.json
	return jsonify(content), 200



if __name__ == '__main__':
	app.run(host='127.0.0.1', port=8080, debug=True)