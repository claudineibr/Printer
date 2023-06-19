import socket
import time
from typing import Optional

from ._NetworkDevice import NetworkDevice


class NetworkPrinterDevice(NetworkDevice):

    def __init__(self, printer_ip: str, printer_port: int, sleep_after_print: Optional[int]) -> None:
        super(NetworkPrinterDevice, self).__init__(printer_ip, printer_port)
        self.sleep_after_print_in_seconds = 0
        if sleep_after_print > 0:
            self.sleep_after_print_in_seconds = (sleep_after_print / 1000.0) + 0.001

    def write(self, data: bytes) -> None:

        try:
            self.socket.sendall(data)
            self.socket.sendall(b"\n\n\n\n\n\n\n\n\x1dV\x00")
        except (socket.error, AttributeError):
            print("Error write data")

    def disconnect(self) -> None:

        time.sleep(self.sleep_after_print_in_seconds)
        super(NetworkPrinterDevice, self).disconnect()
