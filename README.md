# Environment-Sensor-HAT
This repository will document the process of collecting data output from an [Enviornment Sensor HAT](https://www.waveshare.com/environment-sensor-hat.htm) and storing it in csv files. 

A quick synopsis of the Enviornment Sensor HAT:
  - Designed for a Raspberry Pi and uses the simple I2C bus for communication with the Pi.
  - Sensors Onboard:
      - TSL25911FN digital ambient light sensor, for measuring IR and visible light
      - BME280 sensor, for measuring temperature, humidity, and air pressure
      - MPU9250 motion sensor, accelerometer, gyroscope, and magnetometer
      - LTR390-UV-1 sensor, for measuring UV rays
      - SGP40 sensor, for detecting ambient VOC
   
# Running With Docker
   - First, install docker:
     ```
     sudo apt install docker.io
     ```
   - Clone the github repository:
     ```
     git clone https://github.com/NAU-IoT/Environment-Sensor-HAT.git
     ```
   - Change into the directory:
     ```
     cd Enviornment-Sensor-HAT/
     ```
   - Build the docker image:
     ```
     docker build -t sensorhat .
     ```
   - Make a directory to store the docker volume you will create in the next step. For example:
     ```
     mkdir -p Data/SensorV
     ```
   - Create the docker volume:
     ```
     docker volume create --driver local \
         --opt type=none \
         --opt device=/PATHWAY/TO/Data/SensorV \
         --opt o=bind \
         YOUR_VOLUME_NAME
    
  - Run the docker container:
    ```
    docker run --privileged -v YOUR_VOLUME_NAME:/Data -t -i -d sensorhat
    ```
  - Make sure the docker container is running:
    ```
    docker ps
    ```

# Resources
Specifications, dimensions, and pin layouts can be found [here](https://www.waveshare.com/environment-sensor-hat.htm) towards the bottom of the webiste. 

How to Use, Download Demos, and datasheets for the sensors can be found [here](https://www.waveshare.com/wiki/Environment_Sensor_HAT).
  - Note: The Sensor python scripts have been adjusted in this repository to add various fixes and implementations. 
  - VOC Gas Index Algorithm implemented in the SGP40 script can be found [here](https://github.com/Sensirion/gas-index-algorithm/blob/master/python-wrapper/README.rst).
