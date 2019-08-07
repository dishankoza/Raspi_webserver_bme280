from Adafruit_BME280 import *
import sys
import sqlite3
import smtplib, ssl

port = 587  # For starttls
smtp_server = "smtp.gmail.com"
sender_email = "oza.dishank1@gmail.com"
receiver_email = "oza.dishank1@gmail.com"
password = "Charli44$"


def log_values(temp,hum,pressure):
	conn=sqlite3.connect('/var/www/lab_app/lab_app.db')  
	curs=conn.cursor()
	curs.execute("""INSERT INTO data values(datetime(CURRENT_TIMESTAMP, 'localtime'),
         (?), (?),(?))""", (temp,hum,pressure))
	conn.commit()
	conn.close()

sensor = BME280(t_mode=BME280_OSAMPLE_8, p_mode=BME280_OSAMPLE_8, h_mode=BME280_OSAMPLE_8)

temperature = sensor.read_temperature()
pascals = sensor.read_pressure()
pressures = pascals / 100
humidity = sensor.read_humidity()
#print(type(temperature))
if temperature >32:
	message = """
	Subject: Temperature rising
	Temperature>35."""

	context = ssl.create_default_context()
	with smtplib.SMTP(smtp_server, port) as server:
		server.ehlo()  
		server.starttls(context=context)
		server.ehlo()  
		server.login(sender_email, password)
		server.sendmail(sender_email, receiver_email, message)

if humidity is not None and pascals is not None and temperature is not None:
	log_values(temperature,humidity,pressures)
else:
	log_values(999,999,999)
