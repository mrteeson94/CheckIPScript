# Tyson Nguyen | tyson.nguyen@studytafensw.edu.au
# Copyright @Red Opal Innovations
# Proprietary License
# Last Updated: 27/09/23
# Version 1.0.1
# Status 'Development'

# 1. Def and set MAIN() Function to execute all logic
# 1.1 Assign variable to take inputs (IP network e.g:'192.168.0' + mask e.g'255.255.255.0')
# 1.2 Feed var in Validate_input's param for validation check
# 1.3 Assign var to list of ports obtained from Read_ports function


def main():
    status = True
    while status:
        ip_network = input("Enter subnet prefix (e.g: 192.168.0): ")
        subnet_mask = input("Enter subnet mask (e.g: 255.255.255.0): ")
        if validate_input(ip_network, subnet_mask):
            print("Your IP provided is valid!")
            status = False
            ports = read_ports_file()
            print("The file contains the following ports:", ports)

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

# 5. Ip address generation |

# 6.

# 7.

# 8.


main()
