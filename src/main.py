# coding=utf-8
import base64
import json
import os

from printer.interactor.printer_interactor import PrintInteractor
from src.externals.device import NetworkPrinterDevice


def main():
    try:
        with open("../config/config.json", "rb") as f:
            config = json.loads(f.read())
            printer_ip = config.get("printerIp", None)
            printer_port = config.get("printerPort", None)

            if (printer_ip or printer_port) in [None, '']:
                print("Invalid printer IP: {} and/or pinter PORT: {}".format(printer_ip, printer_port))

            sleep_after_print = config.get("MillisecondsSleepAfterPrint", None)
            _build_singletons(printer_ip=printer_ip, printer_port=printer_port, sleep_after_print=sleep_after_print)
    except Exception as ex:
        print("Error Opening file: {}".format(ex.args[0]))


def _build_singletons(printer_ip: str, printer_port: int, sleep_after_print: int) -> None:
    network_printer_device = NetworkPrinterDevice(
        printer_ip=printer_ip,
        printer_port=printer_port,
        sleep_after_print=sleep_after_print,
    )
    _start_print(network_printer_device=network_printer_device)


def _start_print(network_printer_device: NetworkPrinterDevice) -> None:

    print_interactor = PrintInteractor(writer_device=network_printer_device)
    dir_list = os.listdir("../files")
    for x in dir_list:
        if not x.endswith(".txt"):
            continue
        try:
            file_path = "../files/{}".format(x)
            with open(file_path, "r+b") as f:
                data = f.read()
                data = base64.decodebytes(data)
                print_interactor.print_data(data=data)
        except Exception as ex:
            print("Error print data: {}".format(ex.args[0]))


if __name__ == '__main__':
    main()
