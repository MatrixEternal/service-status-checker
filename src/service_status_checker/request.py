import time
import requests
import arguments


request_method = "head"
default_protocol = "http"
args = arguments.initialize_arguments()
interval = float(args.interval)

def main_loop():
    while True:
        time.sleep(
            interval - (time.time() % interval)
        )

        try:
            for service in args.services:
                output(service)
        except Exception as e:
            print(e)
            return


def output(service: str) -> None:
    colors = {
        'red': '\033[31m',
        'color_end': '\033[m',
        'green': '\033[32m',
        'yellow': '\033[33m',
        'blue': '\033[34m'
    }
    time_now = time.localtime()
    time_now = time.strftime("%H:%M:%S", time_now)

    if is_service_online(str(service)):
        print(
            colors["green"] + "[OK]" + colors["color_end"],
            "HTTP service [{}] is available @{}\n".format(service, colors["yellow"] + time_now + colors["color_end"])
        )
    else:
        print(
            colors["red"] + "[error]" + colors["color_end"],
            "HTTP service [{}] unavailable @{}\n".format(service, colors["yellow"] + time_now + colors["color_end"])
        )


def is_service_online(service: str) -> bool:
    address = handle_address(service)

    request = make_request(address)

    return request.status_code == 200 and \
           not request.is_redirect


def handle_address(definition: str) -> str:
    delimiter = "://"

    if delimiter not in definition:
        address = default_protocol + delimiter + definition
    else:
        address = definition

    return address



def make_request(address: str):
    ssl = True
    if args.disable_ssl:
        ssl = False

    request = requests.request(
        request_method,
        address,
        timeout=5,
        verify=ssl
    )

    return request

