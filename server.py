from flask import Flask, jsonify, request
import requests, json, ephem, subprocess, sys, crython
from time import strftime, localtime
from datetime import datetime, timedelta
import re

app = Flask(__name__)

url = 'http://celestrak.com/NORAD/elements/visual.txt'

my_lat = '51.5033630'
my_lon = '-0.1276250'

satellite_bodies = {}
TLE_array = {}

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
	print('-------------------')
	latitude = params['latitude']
	longitude = params['longitude']
	time = params['time']
	parsed_time = parse_time(time)
	# print latitude, longitude, time
	#observer
	query_satellites()
	obs = ephem.Observer()
	obs.lat, obs.lon = latitude, longitude
	obs.date = parsed_time
	
	#TLEs
	visible = []
	for key, body in satellite_bodies.iteritems():
		info = obs.next_pass(body)
		rise_time = info[0].datetime()
		if (rise_time != None) and (rise_time > datetime.now()) and (rise_time < datetime.now() + timedelta(hours=24)):
			visible.append(key)
	EDB = {}
	for sat in visible:
		TLE = TLE_array[sat]
		EDB[sat] = subprocess.check_output(['./tle2edb.py', TLE[0], TLE[1], TLE[2]]).strip()
	response = jsonify(EDB)
	response.status_code = 200
	return response

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

	# print year, month, day, hour, minute, second, tzinfo

if __name__ == '__main__':
	crython.tab.start()
	app.run(debug=True)