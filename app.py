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
def parse_doc():
	content = request.json
	
	for room in content['rooms']:
		room['artifacts'] = [
			{'type':'text', 'text':'{} Artifact. This is the MOST important artifact.'.format(room['name'])},
			{'type':'image', 'url':'https://static.designboom.com/wp-content/uploads/2018/04/cat-VR-isobar-designboom-600.jpg'}
		]
		if 'subRooms' in room:
			for subroom in room['subRooms']:
				subroom['artifacts'] = [
					{'type':'text', 'text':'Subroom Artifact'},
					{'type':'image', 'url':'https://images.pexels.com/photos/1108099/pexels-photo-1108099.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500'}
				]
	

	return jsonify(content), 200


if __name__ == '__main__':
	app.run()