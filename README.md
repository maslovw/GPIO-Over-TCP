# Info
Python script to control GPIO over TCP
TCP server can run on RaspberryPi. Server side 
uses `gpio` command, client adds argument `-g` to the pin number

# Requierements
Python 3

# Requierements for raspberry-pi
RaspberryPi with socat and user permissions for /dev/gpio
`sudo apt-get install wiringpi, socat`

# Client Installation
pip install -e .

# RaspberryPi configuration
Copy folder gpio_server to your bin folder, or add it in PATH
Add to your /etc/rc.local code to run gpio_server/start_server.sh

# Usage
```
>python -m gpio_over_tcp --help
usage: __main__.py [-h] [--host HOST] [--port PORT]
                   [-v {debug,info,warn,error,fatal}]
                   {set,reset,toggle,status,out,in} pin [pin ...]

GPIO control over TCP

positional arguments:
  {set,reset,toggle,status,out,in}
                        'out', 'in' - set pin mode: output or input;
                        'set','reset','toggle' to set desired value on the pin
                        'status' to read current status of the pins
  pin                   pin number(s) to control (can be a list, separated by space)

optional arguments:
  -h, --help            show this help message and exit
  --host HOST           host name or IP address, 
                        env_var "GPIO_HOST:host;port" is used for default
  --port PORT           TCP port for connection
  -v {debug,info,warn,error,fatal}, --verbose {debug,info,warn,error,fatal}
                        logger level, default: error
```

You can create envirenment variable `GPIO_HOST` with value `host address;port`
e.g.: `export GPIO_HOST="localhost;5001"`, in that case you don't need to specify
arguments --host and --port

# Examples
```
> python -m gpio_over_tcp status 16 12
pin_16(16): OUT | High
pin_12(12): OUT | High

>python -m gpio_over_tcp toggle 16 12

>python -m gpio_over_tcp status 16 12
pin_16(16): OUT | Low
pin_12(12): OUT | Low
```
