import os
import datetime
import csv
import time
import ICM20948 #Gyroscope/Acceleration/Magnetometer
import BME280   #Atmospheric Pressure/Temperature and humidity
import LTR390   #UV
import TSL2591  #LIGHT
import SGP40
from PIL import Image,ImageDraw,ImageFont
import math
import socket
import logging
import subprocess

# This will enable logging
log_file = '/Data/logs/waveshare-{}.log'.format(datetime.datetime.now().strftime('%Y%m%d'))
logging.basicConfig(filename=log_file, level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')

def create_csv(filename, headers):
    f_exists= os.path.exists(filename)
    if(f_exists):
        return open(filename, 'a', newline='')

    else:
        with open(filename, 'w', newline='') as file:
           writer = csv.DictWriter(file, fieldnames=headers)
           writer.writeheader()
        return open(filename, 'a', newline='')

def create_data_path():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_dir, 'Data', 'csv_files')
    os.makedirs(data_path, exist_ok=True)
    return data_path

def generate_filename(data_path):
    now = datetime.datetime.now()
    datestamp = now.strftime("%Y-%m-%d")
    filename = os.path.join(data_path, "waveshare-" + datestamp + ".csv")
    return filename

def main():
    logging.info("Starting the program...")

    bme280 = BME280.BME280()
    bme280.get_calib_param()
    light = TSL2591.TSL2591()
    uv = LTR390.LTR390()
    sgp = SGP40.SGP40()
    icm20948 = ICM20948.ICM20948()

    system_hostname = socket.gethostname()

    headers = ['timestamp', 'hosts', 'pressure (hPa)', 'temp (\u00b0C)', 'hum (%RH)', 'light (lux)', 'uv (nm)', 'gas (VOC index)', 'roll (\u00b0)', 'pitch (\u00b0)', 'yaw (\u00b0)', 'acceleration_x (g)', 'acceleration_y (g)', 'acceleration_z (g)', 'gyroscope_x (\u00b0/sec)', 'gyroscope_y (\u00b0/sec)', 'gyroscope_z (\u00b0/sec)', 'magnetic_x (\u00b5T)', 'magnetic_y (\u00b5T)', 'magnetic_z (\u00b5T)']

    data_path = create_data_path()
    filename = generate_filename(data_path)
    csvfile =  create_csv(filename, headers)
    writer = csv.DictWriter(csvfile, fieldnames=headers)

    try:
            logging.info("Reading sensor data...")

            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            time.sleep(1)
            bme = bme280.readData()
            pressure = round(bme[0], 2)
            temp = round(bme[1], 2)
            hum = round(bme[2], 2)
            lux = round(light.Lux(), 2)
            UVS = uv.UVS()
            gas_bytes = subprocess.check_output(["python3", "/SGP40.py"])
            gas_str = gas_bytes.decode('utf-8').strip()

            print("gas str:", gas_str)
            icm = icm20948.getdata()
            
            data = {
                    'timestamp': current_time,
                    'hosts': system_hostname,
                    'pressure (hPa)': pressure,
                    'temp (\u00b0C)': temp,
                    'hum (%RH)': hum,
                    'light (lux)': lux,
                    'uv (nm)': UVS,
                    'gas (VOC index)': gas_str,
                    'roll (\u00b0)': icm[0],
                    'pitch (\u00b0)': icm[1],
                    'yaw (\u00b0)': icm[2],
                    'acceleration_x (g)': icm[3],
                    'acceleration_y (g)': icm[4],
                    'acceleration_z (g)': icm[5],
                    'gyroscope_x (\u00b0/sec)': icm[6],
                    'gyroscope_y (\u00b0/sec)': icm[7],
                    'gyroscope_z (\u00b0/sec)': icm[8],
                    'magnetic_x (\u00b5T)': icm[9],
                    'magnetic_y (\u00b5T)': icm[10],
                    'magnetic_z (\u00b5T)': icm[11]
                }

            logging.info("Writing data to CSV file..")
            writer.writerow(data)

    except KeyboardInterrupt:
        pass

    csvfile.close()
    logging.info("Program finished.")
main()
