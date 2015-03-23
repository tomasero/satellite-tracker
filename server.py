from flask import Flask, jsonify, request
import requests, json, ephem, subprocess, sys, crython
from time import strftime, localtime
from datetime import datetime, timedelta
# from flask_restful import reqparse

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
	# data = request.data
	print('-------------------')
	return request.json
	# print(data)
	# print(data['latitude'])
	# print(request.get_json(force=True))
	# print jsonify(request.data)['latitude']
	# req_latitude = request.data['latitude']
	# req_longitude = request.data['longitude']
	# req_time = request.data['time']
	# print req_latitude, req_longitude, req_time
	# return request.args
	# #observer
	# query_satellites()
	# obs = ephem.Observer()
	# obs.lat, obs.lon = my_lat, my_lon
	# obs.date = strftime("%Y-%m-%d %H:%M:%S", localtime())

	# #TLEs
	# visible = []
	# for key, body in satellite_bodies.iteritems():
	# 	info = obs.next_pass(body)
	# 	rise_time = info[0].datetime()
	# 	if (rise_time != None) and (rise_time > datetime.now()) and (rise_time < datetime.now() + timedelta(hours=24)):
	# 		visible.append(key)
	# EDB = {}
	# for sat in visible:
	# 	TLE = TLE_array[sat]
	# 	EDB[sat] = subprocess.check_output(['./tle2edb.py', TLE[0], TLE[1], TLE[2]]).strip()
	# response = jsonify(EDB)
	# response.status_code = 200
	# return response

if __name__ == '__main__':
	crython.tab.start()
	app.run(debug=True)