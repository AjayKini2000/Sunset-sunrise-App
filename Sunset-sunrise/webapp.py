import json
import requests

from flask import Flask
from flask import render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')



def get_details(lat,lng):
	
	
	base_url = "https://api.sunrise-sunset.org/json?"   
	complete_url = base_url + "&lat=" + lat + "&lng=" + lng
	response = requests.get(complete_url) 

	api_response_dict = response.json()
	if api_response_dict["status"] == "INVALID_REQUEST":
		return render_template('page_not_found.html')

	details = api_response_dict["results"]

	sunrise=details['sunrise']
	sunset=details['sunset']
	solar_noon=details['solar_noon']
	day_length=details['day_length']

	
	# Tuple packing/ Adding all necessary fields
	details_tuple = (sunrise, sunset, solar_noon, day_length)
	return details_tuple

@app.route("/process/", methods=['POST'])
def display_details():

	lat = request.form["lat"]
	lng = request.form["lng"]
	details_tuple = get_details(lat,lng)
	try:
		# Tuple unpacking
		# For 404 page, the tuple will have contents of the page_not_found.html and throws ValueError
		(sunrise, sunset, solar_noon, day_length) = details_tuple
		return render_template(
			'display.html', sunrise=sunrise, sunset=sunset, solar_noon=solar_noon, day_length=day_length)
	except ValueError:
		return details_tuple

if __name__ == '__main__':
	# Remove "debug = True" when deployed in production 
    app.run(debug = True)