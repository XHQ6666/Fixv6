import os
import time
import logging
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

ipv4_target_address = config.get('IP', 'target_ipv4_address')
ipv6_target_address = config.get('IP', 'target_ipv6_address')

log_file = 'debug.log'
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

def ping(address, ip_version):
    response = os.system(f"ping -{ip_version} -n 1 {address}")
    return response

def execute_command(command):
    os.system(command)

def check_and_execute(ip_version, target_address):
    response = ping(target_address, ip_version)
    if response != 0:
        message = f"IPv{ip_version} unavailable, refreshing..."
        logging.info(message)
        execute_command("netsh interface ipv6 set global randomizeidentifiers=disabled & netsh interface ipv6 set global randomizeidentifiers=enabled")
        logging.info("Done")
    else:
        print("IPv6 is available, skip")

consecutive_failures = 0

while True:
    ipv4_response = ping(ipv4_target_address, "4")
    if ipv4_response == 0:
        network_available = True
    else:
        network_available = False

    if network_available:
        print("IPv4 is available, check IPv6")
        check_and_execute(6, ipv6_target_address)
        consecutive_failures = 0
    else:
        logging.info("Network error, please check your Internet connection and make sure it is working")
        consecutive_failures += 1

        if consecutive_failures >= 3:
            logging.info("Many network errors occurred during this time, try again later")
            time.sleep(540)

    time.sleep(60)
