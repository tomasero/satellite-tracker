from flask import Flask
import requests, json, ephem, subprocess, sys
from time import strftime, localtime
from datetime import datetime, timedelta
app = Flask(__name__)

url = 'http://celestrak.com/NORAD/elements/visual.txt'

my_lat = '51.5033630'
my_lon = '-0.1276250'

@app.route('/', methods=['GET'])
def hello_world():

	#observer
	obs = ephem.Observer()
	obs.lat, obs.lon = my_lat, my_lon
	obs.date = strftime("%Y-%m-%d %H:%M:%S", localtime())

	#TLEs
	resp = requests.get(url).content
	resp = map(str.strip, resp.split('\r\n'))
	TLE_array = {}
	for i in xrange(0, len(resp)-1, 3):
		TLE_array[resp[i]] = resp[i:i+3]
	bodies = {}

	#bodies
	for sat, TLE in TLE_array.iteritems():
		bodies[sat] = ephem.readtle(TLE[0], TLE[1], TLE[2])

	visible = []
	for key, body in bodies.iteritems():
		info = obs.next_pass(body)
		rise_time = info[0].datetime()
		if (rise_time != None) and (rise_time > datetime.now()) and (rise_time < datetime.now() + timedelta(hours=24)):
			visible.append(key)
	

	p = subprocess.Popen(["perl", "tle2edb.pl"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
	for sat in visible:
		tle = '\r\n'.join(TLE_array[sat])
		##pipe.stdin.write(tle)
		##print sys.stdin.read()
		output, unused = p.communicate(tle)
		print output
	pipe.stdin.close()

	# print bodies

if __name__ == '__main__':
	app.run(debug=True)