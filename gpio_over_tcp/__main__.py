import argparse
import logging
import os

from gpio_over_tcp.GPIO_control import GpioControl


def parse_args():
    aparse = argparse.ArgumentParser(description='GPIO control over TCP')
    host = os.environ.get('GPIO_HOST')
    if host is None:
        host = 'localhost:5001'
    host_name,host_port = host.split(';')
    aparse.add_argument(
        '--host',
        type=str,
        help='host name or IP address, env_var "GPIO_HOST:host;port" is used for default',
        default=host_name
    )
    aparse.add_argument(
        '--port',
        type=int,
        help='TCP port for connection',
        default = host_port
    )
    aparse.add_argument(
        'action',
        choices=['set', 'reset', 'toggle', 'status', 'out', 'in'],
        type=str,
        help="actions: 'out', 'in' - set mode output or input; "
             "'set','reset','toggle' to set desired value on the pin; "
             "'status' to read current status of the pin"
    )
    aparse.add_argument(
        'pin',
        type=int,
        help='pin number(s) to control',
        nargs='+'
    )
    aparse.add_argument(
        '-v', '--verbose',
        choices=['debug', 'info', 'warn', 'error', 'fatal'],
        type=lambda c: c.lower(),
        help='logger level, default: error',
        default='error'
    )

    args = aparse.parse_args()
    logging.basicConfig(level=args.verbose.upper())
    return args

def execute_action(args):
    pins = {'pin_'+str(x): x for x in args.pin }
    gpio = GpioControl(initialize_pins=False, host=args.host, port=args.port,
                       # pins={pin: args.pin[0]})
                       pins=pins)
    action = args.action
    if action == 'set':
        for pin in pins.keys():
            gpio.set_pin(pin, 1)
    elif action == 'reset':
        for pin in pins.keys():
            gpio.set_pin(pin, 0)
    elif action == 'toggle':
        for pin in pins.keys():
            gpio.toggle_pin(pin)
    elif action == 'out':
        for pin in pins.keys():
            gpio.set_mode(pin, 'OUT')
    elif action == 'in':
        for pin in pins.keys():
            gpio.set_mode(pin, 'IN')
    elif action == 'status':
        answer = gpio.get_pins_state()
        if answer:
            for pin_name, state in answer.items():
                print("{}({}): {} | {}".format(pin_name, gpio.pins[pin_name], state[0], state[1]))
        else:
            print("{empty}")


args = parse_args()
execute_action(args)
