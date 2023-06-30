from src.externals.device import NetworkPrinterDevice


class PrintInteractor(object):
    def __init__(self, writer_device: NetworkPrinterDevice) -> None:
        self.writer_device = writer_device

    def print_data(self, data: bytes) -> None:
        try:

            self.writer_device.initialize()
            self.writer_device.connect()

            status = self.writer_device.get_status()
            if status != 1:
                print("Not connected")
                return

            self.writer_device.write(data)
            return
        except Exception as ex:
            print("Error print: {}".format(ex.args[0]))
        finally:
            self.writer_device.disconnect()
