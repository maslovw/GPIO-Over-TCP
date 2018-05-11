import socket as tcp
import logging

logger = logging.getLogger('GpioConnection')
#
class Connection():
    def __init__(self, host=None, port=None):
        self.socket = tcp.socket(tcp.AF_INET, tcp.SOCK_STREAM, 0)
        self.socket.settimeout(5)
        self.socket.setblocking(0)
        self.is_connected = False
        if host and port:
            self.connect(host, port)


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __del__(self):
        self.close()

    def connect(self, host, port):
        if self.socket and not self.is_connected:
            try:
                self.socket.connect((host, port))

            except tcp.timeout:
                logger.error('Conneciton failed {} {}'.format(host, port))
                raise tcp.timeout("{} {}".format(host, port))
            self.is_connected = False
            try:
                answ = self.socket.recv(7)
            except Exception as e:
                logger.error(" {}. connection failed".format(e))
                self.is_connected = False
                return False
            if b'hi' in answ:
                self.is_connected = True
                logger.debug("Connection established")
        return self.is_connected

    def close(self):
        if self.is_connected:
            self.socket.close()
            self.is_connected = False

    def send_command(self, command):
        if not self.is_connected:
            return None
        try:
            res = self.socket.send(bytes(command+'\r\n', 'utf-8'))
            if res != len(command)+2:
                logger.error("Send command '{}' failed: res = {}".format(command, res))
            answer = self.socket.recv(4096)
        except Exception as e:
            logger.error("Send command '{}' failed".format(command))
            logger.error(e)
            return None
        return answer.decode('utf-8').strip()
