# Tyson Nguyen | tyson.nguyen@studytafensw.edu.au
# Copyright @Red Opal Innovations
# Proprietary License
# Last Updated: 27/09/23
# Version 1.0.1
# Status 'Development'
import pyfiglet
import socket
import os
import win32evtlogutil
import win32con
import time

# 1. Def and set MAIN() Function to execute all logic
# 1.1 Assign variable to take input prompt for ipaddress and subnet
# 1.2 Feed var in Validate_input's param for validation check
# 1.3 Assign var to list of ports obtained from Read_ports function
# 1.4 Ask user for range to assign IP addresses to host devices.
# 1.5 Receive a list of all valid IPv4 addresses
# 1.6 FOR each ipaddress print + log file and log event log viewer


def main():
    display_banner()
    status = True
    while status:
        ip_network = input("Enter subnet prefix (e.g: 192.168.0): ")
        if validate_input(ip_network):
            print("Your IP provided is valid!")
            status = False

            ports = read_ports_file()
            print("The file contains the following ports:", ports)

            print("please only provide numbers in range 1-254")
            new_ipaddress_list = generate_ip_address(ip_network)
            print(new_ipaddress_list)

            for ip_address in new_ipaddress_list:
                open_status, close_status, unavail_status = (
                    port_scan(ip_address, ports)
                )
                print(f"{ip_address} port status-"
                      f"open:{open_status}, "
                      f"closed{close_status}, "
                      f"unavailable:{unavail_status}")
                # log messages + events on console, event viewer
                logging_port_status(
                    ip_address,
                    open_status,
                    close_status,
                    unavail_status
                )
                log_to_event_viewer(ip_address)
        else:
            print(f"Invalid IP/subnet mask, "
                  f"please provide correct address details")


# 2.Validate_input Function check each octet is in range 0-255
# 2.1 Check if there's 3 dots for both IP network and mask
# (possibility of '/24' is given or a complete IPv4 provided)
# 2.2 Check for valid range per octet 0-255
# return true (if all cond is met)


def validate_input(input_network):
    network_parts = list(map(int, input_network.split('.')))
    if len(network_parts) != 3:
        return False

    for part in network_parts:
        try:
            part_in_int = int(part)
            if not 0 <= part_in_int <= 255:
                print("octet is out of range(0-255)")
                return False
        except ValueError:
            print("wrong network address provided,"
                  "please provide valid network address,"
                  "e.g. 192.168.1")
    return True


# 3.Validate_file Function can assume correct port numbers are provided in file
# return true (if all cond is met)

def read_ports_file():
    port_list = []
    ports_file = "ports.txt"
    with open(ports_file, "r") as file:
        for line in file:
            try:
                port = int(line.strip())
                port_list.append(port)
            except Exception as e:
                print(f"An error has occurred while reading file: {str(e)}")
                print("Please check your port.txt file and fix the issue")
    return port_list


# 4.Ip generation assign host no. to complete the IP address within user range
# Rules: Skip first 10 and skip even number


def generate_ip_address(ip_network):
    ipaddress_list = ["127.0.0.1"]
    # for num in range(1, 254):
    #     if num > 10 and num % 2 != 0:
    #         new_ipaddress = ip_network + '.' + str(num)
    #         print(new_ipaddress)
    #         ipaddress_list.append(new_ipaddress)

    return ipaddress_list

# 6. Port_scan Function per IP with list of ports return port status
# TRY connect_ex(ip, port), 0 == open port, erno.ECONNREFUSED (closed), erno.ETIMEOUT (unavilable)


def port_scan(ip_address, ports):
    open_ports = []
    close_ports = []
    unavailable_ports = []

    for port in ports:
        # Attempt to connect to the port
        try:
            # INET = IPv4 internet connection \\ SOCK_STREAM = TCP socket
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.settimeout(5)
            # result = client_socket.connect_ex((ip_address, port))
            client_socket.connect((ip_address, port))
            open_ports.append(port)
            print(f"[{port}] is open")
            client_socket.close()

        except socket.timeout as e:
            print(f"[{port} isn't available], reason: {str(e)}")
            unavailable_ports.append(port)

        except ConnectionRefusedError as e:
            close_ports.append(port)
            print(f"[{port}] is closed, reason: {str(e)}")

    return open_ports, close_ports, unavailable_ports


# 7. Logging ipaddress and all associated port status with that IPv4
def logging_port_status(ip_address, open_status, close_status, unavail_status):
    script_dir = os.path.dirname(os.path.abspath("CheckIPPort.py"))
    log_file = os.path.join(script_dir, f"{ip_address}_port_log.txt")

    with open(log_file, "w") as file:
        file.write(f"Port Status for {ip_address}\n")

        file.write("Open ports:\n")
        for port in open_status:
            file.write(f"{port}\n")

        file.write("Closed ports:\n")
        for port in close_status:
            file.write(f"{port}\n")

        file.write("Unavailable ports:\n")
        for port in unavail_status:
            file.write(f"{port}\n")


# 8. logging the ipaddress to Win Event Log

def log_to_event_viewer(ip_address, event_level="Information"):
    event_source = "IP_Port_Scanner"
    event_id = int(time.time())
    event_msg = f"scanned IPv4: {ip_address}"

    event_type_map = {
        "Information": win32con.EVENTLOG_INFORMATION_TYPE,
        "Warning": win32con.EVENTLOG_WARNING_TYPE,
        "Error": win32con.EVENTLOG_ERROR_TYPE,
    }

    log_event_type = event_type_map.get(event_level, win32con.EVENTLOG_INFORMATION_TYPE)

    win32evtlogutil.ReportEvent(
        event_source, event_id,
        eventType=log_event_type,
        strings=[event_msg])
    print(f"{ip_address} has been scanned and logged to event viewer!")


# Extra feature: Application banner title upon application startup


def display_banner():
    banner = pyfiglet.figlet_format("GELO'S PORT SCANNER")
    print(banner)


main()
