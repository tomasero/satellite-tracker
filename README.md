#SatelliteTracker
- Filters visible satellites in the next 24 hours

---

###Components
- Software
	- Flask
	- Crython (job scheduler)
	- Requests: Quering data from Celestrak
		- http://celestrak.com/NORAD/elements/
	- Ephem
- Hardware
	- Satellite tracker
	- Simcom 800L (cellular)

###Team members
- Nick Firmani
- Rundong Tian
- Tomas Vega

###Notes
Test with the following command
	curl --data "latitude=37.877652&longitude=-122.262247&time=15/03/28,06:20:20%2B12" http://localhost:5000/get_satellites_locations	
