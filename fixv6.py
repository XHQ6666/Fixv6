import os
import time
import logging
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

target_ipv6_address = config.get('IPv6', 'target_ipv6_address')

log_file = 'debug.log'
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

def ping_ipv6(address):
    response = os.system(f"ping -6 -n 1 {address}")
    return response

def execute_command(command):
    os.system(command)

def check_and_execute():
    response = ping_ipv6(target_ipv6_address)
    if response != 0: 
        message = "IPv6 is unavailable, refreshing..."
        logging.info(message)
        execute_command("netsh interface ipv6 set global randomizeidentifiers=disabled & netsh interface ipv6 set global randomizeidentifiers=enabled")
        logging.info("done")

while True:
    check_and_execute()
    time.sleep(60) 
