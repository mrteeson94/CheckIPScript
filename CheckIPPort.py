# Tyson Nguyen | tyson.nguyen@studytafensw.edu.au
# Copyright @Red Opal Innovations
# Proprietary License
# Last Updated: 27/09/23
# Version 1.0.1
# Status 'Development'
import pyfiglet
import socket


# 1. Def and set MAIN() Function to execute all logic
# 1.1 Assign variable to take inputs (IP network e.g:'192.168.0' + mask e.g "255.255.255.0")
# 1.2 Feed var in Validate_input's param for validation check
# 1.3 Assign var to list of ports obtained from Read_ports function
# 1.4 Ask user for range to assign IP addresses to host devices.
# 1.5 Receive a list of all valid IPv4 addresses
# 1.6 FOR each ipaddress check open_port status | print console + log message and store event log through win32


def main():
    display_banner()
    status = True
    while status:
        ip_network = input("Enter subnet prefix (e.g: 192.168.0): ")
        subnet_mask = input("Enter subnet mask (e.g: 255.255.255.0): ")

        if validate_input(ip_network, subnet_mask):
            print("Your IP provided is valid!")
            status = False

            ports = read_ports_file()
            print("The file contains the following ports:", ports)

            print("We will now ask you for host ip range, please only provide numbers in range 1-254")
            new_ipaddress_list = generate_ip_address(ip_network)
            print(new_ipaddress_list)

            for ip_address in new_ipaddress_list:
                port_status = port_scan(ip_address, ports)
                print(f"Current open ports for {ip_address}:", port_status)
# log messages + events on console, event viewer
        else:
            print("Invalid IP or subnet mask, please provide input similar to the prompt examples")


# 2.Validate_input Function | check each octet is within range 0-255 for IP prefix
# 2.1 Check if there's 3 dots for both IP network and mask
# (possibility of '/24' is given or a complete IPv4 provided)
# 2.2 Check for valid range per octet 0-255
# return true (if all cond is met)


def validate_input(input_network, input_subnet):
    network_parts = list(map(int, input_network.split('.')))
    subnet_parts = list(map(int, input_subnet.split('.')))

    if len(network_parts) != 3 or len(subnet_parts) != 4:
        return False
    for part in subnet_parts + network_parts:
        if not 0 <= int(part) <= 255:
            print("octet is out of range(0-255)")
            return False
    return True


# 3.Validate_file Function | from requirement brief we can assume correct port numbers are provided
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

# 4. Ip address generation | assign host number to complete the IP address within user range
# Rules: 1. Skip 0-10 (thus start at 11) and 2.skip even number(all generated host ip will be odd)


def generate_ip_address(ip_network):
    ipaddress_list = ["127.0.0.1"]
    min_input = int(input("What is your starting number for host ip address range: "))
    max_input = int(input("What is your ending host ip address number range: "))

    for num in range(min_input, max_input+1):
        if num > 10 and num % 2 != 0:
            new_ipaddress = ip_network + '.' + str(num)
            print(new_ipaddress)
            ipaddress_list.append(new_ipaddress)
    return ipaddress_list

# 6. Port_scan Function per IP address with list of ports from file | return open ports for that ip address
# Need to include port closed and port unavailable for scanning messages and status for port


def port_scan(ip_address, ports):
    open_ports = []

    for port in ports:
        # Attempt to connect to the port
        try:
            # INET = IPv4 internet connection \\ SOCK_STREAM = TCP socket
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.settimeout(1)  # Check on metrics for int
            result = client_socket.connect_ex(ip_address, port)
            # client_socket.connect((ip_address, port))
            if result == 0:
                print(f"[{port}] is open")
            open_ports.append(port)
            client_socket.close()
        except (socket.timeout, ConnectionRefusedError) as e:
            print(f"No connection to client via this port {port}, reason: {str(e)}")
            pass
    return open_ports

# 7. Extra feature: Application banner title upon application startup


def display_banner():
    banner = pyfiglet.figlet_format("PORT SCANNER")
    print(banner)

main()
