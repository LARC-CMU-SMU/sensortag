# collect lux values from CC2650STK

It works on the Raspberry Pi 3 Model B, which includes a Bluetooth Low Energy receiver.
It requires the [TI SensorTag CC2650STK](http://www.ti.com/tool/CC2650STK).


## Setup

```bash
# clone the repository
git clone https://github.com/LARC-CMU-SMU/sensortag
# go to cloned repository
cd sensortag
# create a virtual envirentment
python3 -m venv venv
# activate the virtual envirenment
source venv/bin/activate
# install bluepy
pip install bluepy
```

## Configuration

update the config.py with sensor tag addresses

### `SENSORTAG_ADDRESS`

The MAC address of the SensorTag can obtained by typing the following into the terminal.

```bash
sudo hcitool lescan
```

Turn on the SensorTag. You should see:

```bash
24:71:89:E6:AD:84 CC2650 SensorTag
```

## Run script

```bash
python record2.py
```
