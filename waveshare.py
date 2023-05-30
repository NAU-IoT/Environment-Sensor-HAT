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

def create_csv(filename, headers, directory):
    os.makedirs(directory, exist_ok=True)
    filepath = os.path.join(directory, filename)
    f_exists = os.path.exists(filepath)

    if(f_exists):
       return open(filepath, 'a', newline='')

    else:
         with open(filepath, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
         return open(filepath, 'a', newline='')

def main():
    directory = "csv_files"

    bme280 = BME280.BME280()
    bme280.get_calib_param()
    light = TSL2591.TSL2591()
    uv = LTR390.LTR390()
    sgp = SGP40.SGP40()
    icm20948 = ICM20948.ICM20948()

    now = datetime.datetime.now()

    datestamp = now.strftime("%Y-%m-%d")
    filename = os.path.join("waveshare-" + datestamp + ".csv")
    headers = [ 'timestamp', 'pressure', 'temp', 'hum', 'lux', 'uv', 'gas', 'roll', 'pitch', 'yaw', 'acceleration_x', 'acceleration_y', 'acceleration_z', 'gyroscope_x', 'gyroscope_y', 'gyroscope_z', 'magnetic_x', 'magnetic_y', 'magnetic_z' ]

    csvfile =  create_csv(filename, headers, directory)
    writer = csv.DictWriter(csvfile, fieldnames=headers)


    try:
        while True:
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            time.sleep(1)
            bme = bme280.readData()
            pressure = round(bme[0], 2)
            temp = round(bme[1], 2)
            hum = round(bme[2], 2)
            lux = round(light.Lux(), 2)
            UVS = uv.UVS()
            gas = round(sgp.raw(), 2)
            icm = icm20948.getdata()

            data = {
                    'timestamp': current_time,
                    'pressure': pressure,
                    'temp': temp,
                    'hum': hum,
                    'lux': lux,
                    'uv': UVS,
                    'gas': gas,
                    'roll': icm[0],
                    'pitch': icm[1],
                    'yaw': icm[2],
                    'acceleration_x': icm[3],
                    'acceleration_y': icm[4],
                    'acceleration_z': icm[5],
                    'gyroscope_x': icm[6],
                    'gyroscope_y': icm[7],
                    'gyroscope_z': icm[8],
                    'magnetic_x': icm[9],
                    'magnetic_y': icm[10],
                    'magnetic_z': icm[11]
                }
            writer.writerow(data)

    except KeyboardInterrupt:
        pass

    csvfile.close()

main()
