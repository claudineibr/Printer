# coding=utf-8
import base64
import json
import os

from printer.interactor.printer_interactor import PrintInteractor
from src.externals.device import NetworkPrinterDevice

ROOT_DIR = os.path.abspath(".")


def main():
    try:
        path = './config/config.json'
        if not os.path.exists(path):
            path = '../config/config.json'

        print("Get config files into: {}".format(path))
        with open(path, "rb") as f:
            config = json.loads(f.read())
            printer_ip = config.get("printerIp", None)
            printer_port = config.get("printerPort", None)

            if (printer_ip or printer_port) in [None, '']:
                print("Invalid printer IP: {} and/or pinter PORT: {}".format(printer_ip, printer_port))

            sleep_after_print = config.get("millisecondsSleepAfterPrint", None)
            _build_singletons(printer_ip=printer_ip, printer_port=printer_port, sleep_after_print=sleep_after_print)
    except Exception as ex:
        print("Error Opening file: {}".format(ex.args[0]))

    input("Press ENTER to close")


def _build_singletons(printer_ip: str, printer_port: int, sleep_after_print: int) -> None:
    network_printer_device = NetworkPrinterDevice(
        printer_ip=printer_ip,
        printer_port=printer_port,
        sleep_after_print=sleep_after_print,
    )
    _start_print(network_printer_device=network_printer_device)


def _start_print(network_printer_device: NetworkPrinterDevice) -> None:

    print_interactor = PrintInteractor(writer_device=network_printer_device)

    files_path = './files'
    if not os.path.exists(files_path):
        files_path = '../files'

    print("List files to print into: {}".format(files_path))
    dir_list = os.listdir(files_path)
    for x in dir_list:
        if not x.endswith(".txt"):
            continue
        try:
            file_path = "{}\\{}".format(files_path, x)
            print("Print file: {}".format(file_path))
            with open(file_path, "r+b") as f:
                data = _parse_file(f.read())
                print_interactor.print_data(data=data)
        except Exception as ex:
            print("Error print data: {}".format(ex.args[0]))


def _parse_file(data: bytes) -> bytes:
    try:
        return base64.decodebytes(data)
    except Exception as _:
        return data


if __name__ == '__main__':
    main()
