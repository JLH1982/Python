from scapy.all import ARP, Ether, srp
import socket
import requests
import time
import pandas as pd
import os
import ipaddress


def clear_screen():
    """Clear the screen based on the operating system."""
    os.system("cls" if os.name == "nt" else "clear")


def get_local_ip():
    """Get the local IP address of the machine."""
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return local_ip


def scan_network(ip_range):
    """Scan the network for active devices."""
    # Create an ARP request packet
    arp = ARP(pdst=ip_range)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp

    # Send the packet and receive the response
    result = srp(packet, timeout=5, verbose=0)[0]
    time.sleep(1)  # Delay to slow down between requests

    # Extract the information from the response
    devices = []
    for sent, received in result:
        devices.append({"ip": received.psrc, "mac": received.hwsrc})

    return devices


def get_oui(mac_address):
    """Get the OUI of the MAC address and return manufacturer info."""
    oui = mac_address.upper().replace(":", "")[:6]
    url = f"https://api.macvendors.com/{oui}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            return "Unknown"
    except requests.RequestException:
        return "Unknown"


def main():
    clear_screen()
    local_ip = get_local_ip()

    # Define the IP range in CIDR notation
    ip_network = ipaddress.IPv4Network(f"{local_ip}/24", strict=False)
    ip_range = f"{ip_network.network_address}/{ip_network.prefixlen}"

    print(f"Scanning network: {ip_range}")

    devices = scan_network(ip_range)
    print("Available devices in the network:")
    if not devices:
        print("No devices found.")
    else:
        # Print header
        print(f"{'IP Address':<20} {'MAC Address':<20} {'OUI':<30}")
        print("-" * 70)
        for device in devices:
            oui = get_oui(device["mac"])
            device["oui"] = oui
            # Print each device's information with aligned columns
            print(f"{device['ip']:<20} {device['mac']:<20} {device['oui']:<30}")
            time.sleep(1)  # Add a delay of 1 second between OUI lookups

    # Ask if the user wants to save to an Excel file
    while True:
        save_to_excel = (
            input("Do you want to save the results to an Excel file? ([yes]/no): ")
            .strip()
            .lower()
        )
        if save_to_excel in ["yes", "y", ""]:
            # Prompt for file name if the file already exists
            output_file = "network_scan_results.xlsx"
            if os.path.exists(output_file):
                output_file = input(
                    "File already exists. Enter a new file name: "
                ).strip()
                if not output_file.endswith(".xlsx"):
                    output_file += ".xlsx"
            # Create a DataFrame and save it to an Excel file
            df = pd.DataFrame(devices)
            df.to_excel(output_file, index=False)
            print(f"Results saved to {output_file}")
            break
        elif save_to_excel in ["no", "n"]:
            print("Results not saved.")
            break


if __name__ == "__main__":
    main()
