import time
import os
from threading import Thread
from bluepy.btle import BTLEException
from bluepy.sensortag import SensorTag
from config import SENSOR_TAG_LIST

IR_TEMP = "ir_temp"
ACCELEROMETER = "accelerometer"
HUMIDITY = "humidity"
MAGNETOMETER = "magnetometer"
BAROMETER = "barometer"
GYROSCOPE = "gyroscope"
BATTERY = "battery"
LIGHT = "light"

DEFINED_SENSORS = [IR_TEMP, ACCELEROMETER, HUMIDITY, MAGNETOMETER, BAROMETER, GYROSCOPE, BATTERY, LIGHT]
INTERESTED_SENSORS = [LIGHT, BATTERY]
OUT_FILE = "lux.csv"
TIME_BETWEEN_READS = 5
TIME_BETWEEN_WRITES = 10
TIME_BETWEEN_RETRY = 5

LUX_READINGS = []


def get_light(tag):
    ret = None
    try:
        ret = tag.lightmeter.read()
    except Exception as e:
        print(e)
    return ret


def get_time():
    return int(time.time())


def collect_lux_readings(label, ble_mac):
    print(ble_mac, label, "starting collection thread")
    print(ble_mac, label, "connecting...")
    tag = None
    while not tag:
        try:
            tag = SensorTag(ble_mac)
            tag.lightmeter.enable()
            time.sleep(1.0)
        except Exception as e:
            print(ble_mac, label, str(e))
            print("will retry in %d seconds" % TIME_BETWEEN_RETRY)
            time.sleep(TIME_BETWEEN_RETRY)
    print(ble_mac, label, "connected")

    while 1:
        light = get_light(tag)
        if light:
            reading={"timestamp":get_time(),"lux":light,"label":label}
            LUX_READINGS.append(reading)
        time.sleep(TIME_BETWEEN_READS)


def process_readings():
    print("starting processing thread")
    while 1:
        current_records_number = len(LUX_READINGS)
        if current_records_number > 0:
            if not os.path.isfile(OUT_FILE):
                create_csv_file_with_header(OUT_FILE, sorted(LUX_READINGS[0].keys()))
            i = 0
            with open(OUT_FILE, 'a') as f:
                while i < current_records_number:
                    values = []
                    readings = LUX_READINGS.pop()
                    with open(OUT_FILE, "a") as f:
                        for k in sorted(readings):
                            values.append(readings[k])
                        f.write(",".join([str(x) for x in values]) + "\n")
                    i += 1
        time.sleep(TIME_BETWEEN_WRITES)


def create_csv_file_with_header(file_name, header):
    header_line = ','.join(header)
    print("creating file with header,", header)
    with open(file_name, 'w') as f:
        f.write(header_line + '\n')


def main():
    start_time = int(time.time())
    print('init time', start_time)
    for sensor_tag in SENSOR_TAG_LIST:
        Thread(target=collect_lux_readings, args=(sensor_tag["label"], sensor_tag["ble_mac"])).start()
        time.sleep(1)
    process_readings()


if __name__ == "__main__":
    main()
