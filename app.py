from flask import Flask, request, jsonify
import time, json
import logging

app = Flask(__name__)


#############################################################
# API
#############################################################

@app.route("/")
def api_root():
  return "Malloci API"

#############################################################
# POST /parse
# 	Returns links of all images uploaded with this service
#############################################################
@app.route("/parse",  methods=['POST'])
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