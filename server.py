from flask import Flask, jsonify, request
import requests, json, ephem, subprocess, sys, crython
from time import strftime, localtime
from datetime import datetime, timedelta
import re

app = Flask(__name__)

url = 'http://celestrak.com/NORAD/elements/visual.txt'

satellite_bodies = {}
TLE_array = {}

#how to test cronjob?
#should I run query_satellites once when server is up?
@crython.job(expr='@daily')
def query_satellites():
	resp = requests.get(url).content
	resp = map(str.strip, resp.split('\r\n'))
	for i in xrange(0, len(resp)-1, 3):
		TLE_array[resp[i]] = resp[i:i+3]
	#bodies
	for sat, TLE in TLE_array.iteritems():
		satellite_bodies[sat] = ephem.readtle(TLE[0], TLE[1], TLE[2])

@app.route('/get_satellites_locations', methods=['POST'])
def get_satellites_locations():
	params = request.form
	message = validate_params(params)
	if message != None:
		response = jsonify(message)
		response.status_code = 400
		return response

	#extract params
	latitude = params['latitude']
	longitude = params['longitude']
	time = params['time']
	parsed_time = parse_time(time)

	#observer
	query_satellites() #comment out when server running
	obs = ephem.Observer()
	obs.lat = latitude
	obs.lon = longitude
	obs.date = parsed_time
	
	#TLEs
	visible = get_visible_satellites(obs)

	if not visible:
		message = {'status': 200,
					'error': 'No visible satellites available.'}
		response = jsonify(message)
		response.status_code = 200
		return response

	response_objs = get_formatted_response(visible)
	response = jsonify({'objects': response_objs})
	response.status_code = 200
	return response

def get_formatted_response(satellites):
	response_objs = []
	for sat in satellites:
		TLE = TLE_array[sat]
		EDB = subprocess.check_output(['./tle2edb.py', TLE[0], TLE[1], TLE[2]]).strip()
		obj = {
			"satellide_id": TLE[1][2:7],
			"satellite_name": sat,
			"edb": EDB
		}
		response_objs.append(obj)
	return response_objs

def get_visible_satellites(obs):
	visible = []
	for key, body in satellite_bodies.iteritems():
		info = obs.next_pass(body)
		rise_time = info[0].datetime()

		#1 rise within 24
		#2 rise before and end before the 24 hours
		#3 rise before and sets after

		if (rise_time != None) and (rise_time > datetime.now()) and (rise_time < datetime.now() + timedelta(hours=24)):
			visible.append(key)
	return visible

def validate_params(params):
	message = None
	if 'latitude' not in params:
		message = {'status': 400,
					'error': 'Please provide latitude.'}
	if 'longitude' not in params:
		message = {'status': 400,
					'error': 'Please provide longitude.'}
	if 'time' not in params:
		message = {'status': 400,
					'error': 'Please provide time.'}
	return message

def parse_time(time):
	year = int(time[:2])
	if year > datetime.now().year%1000:
		year += 1900
	else:
		year += 2000
	month = int(time[3:5])
	day = int(time[6:8])
	hour = int(time[9:11])
	minute = int(time[12:14])
	second = int(time[15:17])
	operand = time[17]
	zone = int(time[18:21])

	if operand == '+':
		delta = timedelta(hours=zone)
	else:
		delta = timedelta(hours=-zone)
	dt = datetime(year, month, day, hour, minute, second)
	dt = dt + delta
	return dt

if __name__ == '__main__':
	crython.tab.start()
	app.run(debug=True)