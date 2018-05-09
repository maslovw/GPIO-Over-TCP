import logging
import socket as tcp
from gpio_over_tcp.GPIO_tcp_connection import Connection
from typing import Optional


logger = logging.getLogger('GpioControl')

class GpioControl():
    def __init__(self, initialize_pins=True, host=None, port=None, pins=None ):
        # self.pins ={'kl30': 21,
        #               'kl15': 16,
        #               'eth': 12,
        #               'obd': 20}
        self.pins = pins if pins is not None else dict()
        logger.debug(str(pins))
        logger.debug("{}:{}".format(host, port))
        self.connection = Connection(host, port)
        if not self.connection.is_connected:
            logger.error("Can't establish connection with '{}:{}'".format(host, port))
            raise ConnectionError()
        if initialize_pins:
            # self.set_pins_default()
            self.init_pins()

    def __del__(self):
        if self.connection:
            self.connection.close()

    def set_pins_default(self):
        if self.connection.is_connected:
            for name, pin in self.pins.items():
                self.connection.send_command('-g write {} 1'.format(pin))
                self.connection.send_command('-g mode {} out'.format(pin))
                logger.debug('Mode {}:{} is set to "out"'.format(name, pin))

    def toggle_pin(self, pin_name):
        """
        Send command 'toggle'
        :param pin_name: key in the pins dictionary
        :return: True if success
        """
        pin = self.pins.get(pin_name, None)
        if pin:
            result = self.connection.send_command('-g toggle {}'.format(pin))
            logger.debug('Toggle {}[{}]: {}'.format(pin_name, pin, result))
            return result is not None
        else:
            logger.warning('Toggle unknown pins: {}'.format(pin_name))
        return False

    def set_pin(self, pin_name, state=1):
        """
        Send command 'set'
        :param pin_name: key in the pins dictionary
        :param state: 1 for set, 0 for reset
        :return: True if success
        """
        pin = self.pins.get(pin_name, None)
        if pin:
            result = self.connection.send_command('-g write {} {}'.format(pin, 1 if state else 0))
            logger.debug('{} {}[{}]: {}'.format("Set" if state else "Reset",
                pin_name, pin, result))
            return result is not None
        else:
            logger.warning('Set unknown pins: {}'.format(pin_name))
        return False

    def get_pins_state(self)-> Optional[dict]:
        """
        Read all the pins' states described in the pins dictionary
        :return: None if couldn't read the states
        :return: {pin_name: (mode, value)}, where pin_name is a key in pins dict
            mode: ["OUT", "IN"]
            value: [0, 1]
        """
        if self.connection.is_connected:
            answer = self.connection.send_command('allreadall')
            if answer == 'gpio allreadall':
                answer = ""
                while True:
                    try:
                        answer += (self.connection.socket.recv(100).decode('utf-8'))
                    except tcp.timeout:
                        logger.debug("TCP timeout")
                        break
                    except Exception as e:
                        logger.warning(e)
                        return None
                ret = {}
                for name,pin in self.pins.items():
                    found = answer.find('{} |'.format(pin))
                    if found:
                        state_str = answer[found: found + 20].split('|')
                        mode = state_str[1].strip()
                        value = state_str[2].strip()
                        ret[name] = (mode, value)
                return ret
        return None

    def init_pins(self):
        if self.connection.is_connected:
            states = self.get_pins_state()
            if states:
                for pinname, state in states.items():
                    if 'OUT' not in state[0]:
                        pin = self.pins[pinname]
                        result = self.connection.send_command('-g write {} 1'.format(pin))
                        if result is None:
                            logger.error('Can not set pin {}:{} to "1"'.format(pinname, pin))
                            return False

                        result = self.connection.send_command('-g mode {} out'.format(pin))
                        if result is None:
                            logger.error('Can not change Mode {}:{} to "out"'.format(pinname, pin))
                            return False
                        logger.debug('Mode {}:{} is set to "out"'.format(pinname, pin))
                return True
        return False

    def set_mode(self, pin_name, mode):
        '''
        :param mode: 'OUT' or 'IN'
        :return: True if sucess
        '''
        pin = self.pins.get(pin_name, None)
        if pin:
            result = self.connection.send_command('-g mode {} {}'.format(pin, mode))
            logger.debug('Set Mode {} {}[{}]: {}'.format(mode,
                                                pin_name, pin, result))
            return result is not None
        else:
            logger.warning('Set unknown pins: {}'.format(pin_name))
        return False

