from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)


#############################################################
# API
#############################################################

@app.route("/")
def api_root():
  return "Malloci API"

#############################################################
# POST /generate
# 	Returns links of all images uploaded with this service
#############################################################
@app.route("/generate",  methods=['POST'])
@cross_origin()
def parse_doc():
	content = request.json
	
	for room in content['rooms']:
		room['artifacts'] = [
			{'type':'text', 'text':'This is the MOST important artifact.'},
			{'type':'image', 'url':'https://static.designboom.com/wp-content/uploads/2018/04/cat-VR-isobar-designboom-600.jpg'}
		]
	

	return jsonify(content), 200


if __name__ == '__main__':
	app.run()