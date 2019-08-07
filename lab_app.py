from flask import Flask, request, render_template
import sys
from Adafruit_BME280 import *
import sqlite3
import time
import datetime

app = Flask(__name__)
app.debug = True 

#@app.route("/")
#def hello():
 #   return "Hello World!"

@app.route("/lab_temp")
def lab_temp():
	sensor = BME280(t_mode=BME280_OSAMPLE_8, p_mode=BME280_OSAMPLE_8, h_mode=BME280_OSAMPLE_8)


	temperature = sensor.read_temperature()
	pascals = sensor.read_pressure()
	hectopascals = pascals / 100
	humidity = sensor.read_humidity()

	if humidity is not None and temperature is not None and pascals is not None:
		return render_template("lab_temp.html",temp=temperature,hum=humidity,pressure=hectopascals)
	else:
		return render_template("no_sensor.html")

@app.route("/",methods=['GET'])
def lab_env_db():
	sensordata,from_date_str,to_date_str = get_records()
	#return render_template("lab_env_db.html",data=sensordata)
	return render_template(	"lab_env_db.html", 	bmedata 			= sensordata,
							from_date 		= from_date_str, 
							to_date 		= to_date_str,
							data_items 		= len(sensordata))
	

def get_records():
	from_date_str 	= request.args.get('from',time.strftime("%Y-%m-%d 00:00")) #Get the from date value from the URL
	to_date_str 	= request.args.get('to',time.strftime("%Y-%m-%d %H:%M"))   #Get the to date value from the URL
	
	range_h_form	= request.args.get('range_h','');
	range_h_int 	= "nan"  #initialise this variable with not a number

	try: 
		range_h_int	= int(range_h_form)
	except:
		print ("range_h_form not a number")
 	

	if not validate_date(from_date_str):		
		from_date_str 	= time.strftime("%Y-%m-%d 00:00")
	if not validate_date(to_date_str):
		to_date_str 	= time.strftime("%Y-%m-%d %H:%M")

	if isinstance(range_h_int,int):	
		time_now		= datetime.datetime.now()
		time_from 		= time_now - datetime.timedelta(hours = range_h_int)
		time_to   		= time_now
		from_date_str   = time_from.strftime("%Y-%m-%d %H:%M")
		to_date_str	    = time_to.strftime("%Y-%m-%d %H:%M")

	conn=sqlite3.connect('/var/www/lab_app/lab_app.db')
	curs=conn.cursor()
	curs.execute("SELECT * FROM data  WHERE rDateTime BETWEEN ? AND ?", (from_date_str, to_date_str))
	sensordata = curs.fetchall()
	conn.close()
	return [sensordata,from_date_str,to_date_str]

def validate_date(d):
    try:
        datetime.datetime.strptime(d, '%Y-%m-%d %H:%M')
        return True
    except ValueError:
        return False


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)

