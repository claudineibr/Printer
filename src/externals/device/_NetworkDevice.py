import socket

from abc import ABCMeta
from typing import Optional

from src.printer.model import Device

SOCKET_BUF_SIZE = 1
REQUEST_STATUS_CODE = b'\x10\x04\x01'


class NetworkDevice(Device):
    __metaclass__ = ABCMeta

    def __init__(self, printer_ip: str, printer_port: int) -> None:
        self.socket = None  # type: Optional[socket.socket]

        self.printer_ip = printer_ip
        self.printer_port = printer_port

    def get_name(self) -> str:
        return 'NetworkDevice'

    def initialize(self) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(1)

        keep_alive_on = 1
        idle_time_before_keep_alive_seconds = 1000 * 1
        interval_between_keep_alive_packets_seconds = 1000 * 3
        config = (keep_alive_on, idle_time_before_keep_alive_seconds, interval_between_keep_alive_packets_seconds)
        self.socket.ioctl(socket.SIO_KEEPALIVE_VALS, config)

    def connect(self) -> None:
        try:
            self.socket.connect((self.printer_ip, self.printer_port))
        except Exception as e:
            print("Error getting socket connection: [{}]".format(repr(e)))

    def disconnect(self) -> None:
        try:
            try:
                self.socket.shutdown(socket.SHUT_RDWR)
            except socket.error:
                pass
            self.socket.close()
        except Exception as _:
            print("Error closing socket connection")

    def get_status(self) -> int:

        self.socket.sendall(REQUEST_STATUS_CODE)
        bin_status = self.socket.recv(SOCKET_BUF_SIZE)
        bin_status = format(ord(bin_status), '08b')

        if "1" == bin_status[-6]:
            raise IOError()

        if "1" == bin_status[-4]:
            raise IOError()

        return 1
