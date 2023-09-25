# Tyson Nguyen | tyson.nguyen@studytafensw.edu.au
# Copyright @Red Opal Innovations
# Proprietary License
# Last Updated: 27/09/23
# Version 1.0.1
# Status 'Development'

# 1. Def and set MAIN() Function to execute all logic
# 1.1 Assign variable to take inputs (IP network e.g:'192.168.0' + mask e.g'255.255.255.0')
# 1.2 Feed var in Validate_input's param for validation check
# 1.3 Feed i

def main():
    status = True
    while status:
        ip_network = input("Enter subnet prefix (e.g: 192.168.0): ")
        subnet_mask = input("Enter subnet mask (e.g: 255.255.255.0): ")
        if validate_input(ip_network, subnet_mask):
            print("Your IP provided is valid!")
        else:
            print("Invalid IP or subnet mask, please provide input similar to the prompt examples")
            status = False


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
            return False
    return True



# 3.Validate_file Function | check ports.txt is in valid range of 1024-65535
# 3.1 Check for valid range
# 3.2 Check for duplicates
# return true (if all cond is met)

# 4.Generate_IP() |

# 5.

# 6.

# 7.

# 8.


main()
