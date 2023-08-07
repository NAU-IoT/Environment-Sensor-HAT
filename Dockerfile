FROM ubuntu:22.04

RUN apt-get update

RUN apt-get install -y python3 python3-pip python3-smbus python3-rpi.gpio python3-pillow

RUN apt-get -y install cron

RUN mkdir -p /Data/logs

# Install timezone data and setting the time zone
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install tzdata
ENV TZ=America/Phoenix
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ADD waveshare.py /waveshare.py

ADD waveshare.sh /waveshare.sh

ADD TSL2591.py /TSL2591.py

ADD LTR390.py /LTR390.py

ADD SGP40.py /SGP40.py

ADD ICM20948.py /ICM20948.py

ADD BME280.py /BME280.py 

RUN pip install sensirion-gas-index-algorithm

ADD cronjob /etc/cron.d/cronjob

RUN touch /var/log/cron.log

RUN chmod 644 /etc/cron.d/cronjob

RUN chmod +x /waveshare.py

RUN chmod +x /waveshare.sh

RUN chmod +x /TSL2591.py

RUN chmod +x /LTR390.py

RUN chmod +x /SGP40.py

RUN chmod +x /BME280.py

CMD cron && bash
