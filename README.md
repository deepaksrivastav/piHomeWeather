# piHomeWeather
DHT22 based temperature and humidity sensor for the Raspberry Pi

Circuit diagram:
<img src="https://raw.githubusercontent.com/deepaksrivastav/piHomeWeather/master/dht22.jpg" alt="Circuit Diagram" style="width:100px;height:110px">

I am currently using GPIO 4 as input from the circuit.

Installing the driver:
- sudo apt-get update
- sudo apt-get install build-essential python-dev python-openssl
- git clone https://github.com/adafruit/Adafruit_Python_DHT.git
- cd Adafruit_Python_DHT
- sudo python setup.py install

Running the project
This is currently a very simple project which just reports temperature and humidity. Will evolve further.
- sudo ./piHomeWeather.py
