# Environment-Sensor-HAT
This repository will document the process of collecting data output from an [Enviornment Sensor HAT](https://www.waveshare.com/environment-sensor-hat.htm) and storing it in csv files. 

A quick synopsis of the Enviornment Sensor HAT:
  - Designed for a Raspberry Pi and uses the simple I2C bus for communication with the Pi.
  - Sensors Onboard:
      - TSL25911FN digital ambient light sensor, for measuring IR and visible light
      - BME280 sensor, for measuring temperature, humidity, and air pressure
      - ICM20948 motion sensor, accelerometer, gyroscope, and magnetometer
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
     cd Environment-Sensor-HAT/
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
# Calibrating Guide for the SGP40 Sensor
## Required items:
* Tap water
* 200 grams of table salt
* 1 teaspoon of ethanol (40% vol. or more)
* 4 containers with lids approx. the same size. (50-200mL)
* 2 bowls
* 2 large bottles with lids. (1 Liter or more)
## Step 1: Creating Your Saturated Salt Solution
* In `Bottle 1`, mix 200g of salt with a liter of water.
  * Shake the bottle well, most of the salt won't dissolve and will settle at the bottom of the bottle.
## Step 2: Preparing our High VOC Concentration Solution
* In `Bowl 1`, mix 250 mL of the salt solution you made in `Step 1` with 1 teaspoon of ethanol.
* Next, dilute it 10:1 in `Bowl 2` by mixing 2 tablespoons of the solution from `Bowl 1` with 250 mL of `Bottle 1's` solution
* Dilute once more in `Bottle 2` by mixing 2 tablespoons of `Bowl 2's` solution with 250 mL of `Bottle 1's` solution.
  * `Bottle 2` is diluted 100:1, and is now your high concentration solution.
  * Make sure to tightly secure the lid to `Bottle 2` so the ethanol does not evaporate, and the concentration remains constant.
## Step 3: Concentration Series
* Arrange the 4 small empty containers in front of you.
* Fill `Container 1` halfway with the high concentration of `Bottle 2`. Fill `Container's 2-4` halfway with the salt solution of `Bottle 1`
  * The red concentration is filled halfway with the high concentration, whereas the blue concentrations are the salt solutions. 
![Container 1-4 filled halfway](https://i.imgur.com/ilFy8bp.png)

* Fill `Container 2` to full with the high concentration from `Bottle 2`. Stir well.
![Container 2 fully filled fully](https://i.imgur.com/0KubbGQ.png)
* Fill `Container 3` to full with half of the concentration from `Container 2`. Stir well.
![Container 3 fully filled fully](https://i.imgur.com/yF2tcGH.png)
* Fill `Container 4` to full with half of the concentration from `Container 3`. Stir well.
![Container 4 fully filled fully](https://i.imgur.com/hPDDckE.png)
* Discard half of `Container 4`. This is your baseline concentration.
  * Since we started off with the the High concentration solution in `Container 1` and diluted from there, each consecutive container will be half of its preceeding concentration. 
![Containers 1-4 ready](https://i.imgur.com/fDC8vvC.png)
### Note: 
  * In this context, "halfway" does not need to be a specific amount. Just make sure "halfway" remains constant throughout the experiement and "full" is double the amount of "halfway"
  * Make sure to close each container with lids when you are not using them to ensure the ethanol does not evaporate. 
## Step 4: Training the Sensor
* Training 1: Expose the sensor to the baseline concentration (the container with the lowest concentration) for 60 min
* Training 2: Expose the sensors to the high concentration for 15 min
* Training 3: Expose the sensors to the baseline concentration again for 30 min
## Step 5: Verifying the Sensor
* Note: Run the `waveshare.py` script in the background when exposing the sensor to these different concentrations and record the output after each test.
* Test 1: Expose the sensor to the quarter concentration for 5 min.
* Test 2: Epose the sensor to the half concentration for 5 min.
* Test 3: Expose the sensor to the high concentration for 5 min.
* Test 4: Expose the sensor to the baseline concentration for 5 min.

## Results
* Average household VOC index is around 100. Anything above that is less than average VOC quality, and anything below that is above average VOC quality. The range of the sensor is 0-500 VOC index.
* Testing the baseline concentration: 120 VOC index
* Testing the quarter concentration: 130-135 VOC index
* Testing the half concentration: 150-155 VOC index
* Testing the high concentration: 170-173 VOC index
* Testing pure ethanol for calibration purposes: 480 VOC index

# Resources
Specifications, dimensions, and pin layouts can be found [here](https://www.waveshare.com/environment-sensor-hat.htm) towards the bottom of the webiste. 

How to Use, Download Demos, and datasheets for the sensors can be found [here](https://www.waveshare.com/wiki/Environment_Sensor_HAT).
  - Note: The Sensor python scripts have been adjusted in this repository to add various fixes and implementations. 
  - VOC Gas Index Algorithm implemented in the SGP40 script can be found [here](https://github.com/Sensirion/gas-index-algorithm/blob/master/python-wrapper/README.rst).
