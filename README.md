# python-ultimaker-printer-api

An Ultimaker Printer API Client implementation in Python.
Derived from Swagger documentation (see http://printer_ip/docs/api/) and request testing.

## Support

| Printer   | Support | Tested | Notes |
|-----------|---------|--------|-------|
| UM 2+ Con | 🏁      | ❓      |       |
| UM S3     | ✔️      | ❓      |       |
| UM S3     | ✔️      | ❓      |       |

[No local printing](https://support.makerbot.com/s/article/1667412440858)

## API Documentation

* http://[printer_ip_here]/cluster-api/v1/ for printer and print job management.
* http://[printer_ip_here]/docs/api for low-level access to the printer's parameters and system.

Source: https://support.makerbot.com/s/article/1667412427787

## Demo

See https://github.com/vanderbilt-design-studio/poller-pi/blob/master/printers.py.
This powers printer feed retrieval for https://vanderbilt.design/ (scroll down to the bottom).

## Usage

See folder `scripts`.

## mDNS

If your local network supports mDNS (some school/corporate networks disable it), printers can be automatically discovered with the zeroconf package. Use script `mdns.py`.
