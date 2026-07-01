from __future__ import annotations

import logging
import shelve
import socket

from zeroconf import ServiceInfo, ServiceListener

from ultimaker import Identity, Printer


class PrinterListener(ServiceListener):
    def __init__(self, credentials_dict: shelve.Shelf) -> None:
        self.printers_by_name: dict[str, Printer] = {}
        self.credentials_dict: shelve.Shelf = credentials_dict
        self.logger = logging.getLogger(self.__class__.__name__)

    def add_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        info: ServiceInfo = zc.get_service_info(type_, name)
        if len(info.addresses) == 0:
            self.logger.warning(f"Service {name} added but had no IP address, cannot add")
            return
        address = socket.inet_ntoa(info.addresses[0])
        identity = Identity(ultimaker_application_name, ultimaker_user_name)
        credentials = self.credentials_dict.get(str(printer.get_system_guid()), None)  # fixme
        self.printers_by_name[name] = Printer(address, info.port, identity, credentials)
        self.logger.info(f"Service {name} added with guid: {printer.get_system_guid()}")  # fixme

    def remove_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        del self.printers_by_name[name]
        self.logger.info(f"Service {name} removed")

    def update_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        raise NotImplementedError

    def printer_jsons(self) -> list[dict[str, str]]:
        printer_jsons: list[dict[str, str]] = []
        # Convert to list here to prevent concurrent changes by zeroconf affecting the loop
        for printer in list(self.printers_by_name.values()):
            try:
                printer_status_json: dict[str, dict[str, str]] = printer.into_ultimaker_json()
                printer_jsons.append(printer_status_json)  # fixme

                if printer.credentials is not None and str(printer.get_system_guid()) not in self.credentials_dict:
                    self.logger.info(f"Did not see credentials for {printer.get_system_guid()} in credentials, adding and saving.")
                    self.credentials_dict[str(printer.get_system_guid())] = printer.credentials
                    self.credentials_dict.sync()
            except Exception as e:
                if type(e) is KeyboardInterrupt:
                    raise e
                self.logger.warning(f"Exception getting info for printer {printer.get_system_guid()}, it may no longer exist: {e}")
        return printer_jsons


if __name__ == "__main__":
    from zeroconf import ServiceBrowser, Zeroconf

    ultimaker_application_name = "Application"
    ultimaker_user_name = "Anonymous"
    ultimaker_credentials_filename = "./credentials.shelve"

    zeroconf = Zeroconf()
    shelf = shelve.open(ultimaker_credentials_filename)  # noqa: S301 SIM115
    listener = PrinterListener(shelf)
    browser = ServiceBrowser(zeroconf, "_ultimaker._tcp.local.", listener)
    try:
        input("Press enter to exit\n")
    finally:
        print("Exiting...")
        shelf.close()
        zeroconf.close()
