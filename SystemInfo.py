from datetime import datetime
import platform
import subprocess
import sys

# Clearing the terminal screen based on the platform
def clear_screen():
    if sys.platform.startswith('win'):
        subprocess.run(['cls'], shell=True)
    else:
        subprocess.run(['clear'])

# Installing net-tools package for Linux
def install_linux_package(package):
    subprocess.run(['sudo', 'apt', 'update'])
    subprocess.run(['sudo', 'apt', 'install', '-y', package])

# Installing wmic package for Windows.
def install_windows_package(package):
    subprocess.run(['choco', 'install', package, '-y'])

# Gathering system information.
def get_system_info():
    system_info = platform.uname()
    return {
        "Name": system_info.node,
        "System": system_info.system,
        "Release": system_info.release,
        "Version": system_info.version,
        "User": psutil.users(),
        "\n****************** SYSTEM INFO ****************** \nMachine": system_info.machine,
        "Processor": system_info.processor,
        "Processor Speed (MHz)": round(psutil.cpu_freq().current, 2),
        "Physical cores ": psutil.cpu_count(logical=False),
        "Total cores": psutil.cpu_count(logical=True),
        "RAM (GB)": round(psutil.virtual_memory().total / (1024 ** 3), 2),
        "Available RAM (GB)": round(psutil.virtual_memory().available / (1024 ** 3), 2),
        "SWAP (GB)": round(psutil.swap_memory().total / (1024 ** 3), 2),
        "\n********************* DISK ********************* \nDisk Size (GB)": round(psutil.disk_usage('/').total / (1024 ** 3), 2),
        "Used Disk (GB)": round(psutil.disk_usage('/').used / (1024 ** 3), 2),
        "Free Disk (GB)": round(psutil.disk_usage('/').free / (1024 ** 3), 2),
        "\n******************** NETWORK ******************** \nNetwork": get_network_info()
    }

# Gathering Network information. If the system is Linux then tries to run ifconfig and if unable to then will attempt to install net-tools.
# If the system is Windows then it attempts to run ipconfig and if unable to then will attempt to install wmic.
def get_network_info():
    #Linux
    if sys.platform.startswith('linux'):
        try:
            subprocess.run(['ifconfig', '-v'])
            return subprocess.check_output(['ifconfig']).decode()
        except FileNotFoundError:
            print("ifconfig not found. Attempting to install...")
            install_linux_package('net-tools')
            return "Network information installed. Run the script again to view."
        except Exception as e:
            return f"Error retrieving network information: {e}"
    # Windows
    elif sys.platform.startswith('win'):
        try:
            network_info = subprocess.check_output(['ipconfig', '/all']).decode()
            return network_info
        except FileNotFoundError:
            print("ipconfig not found. Attempting to install...")
            install_windows_package('wmic')
            return "Network information installed. Run the script again to view."
        except Exception as e:
            return f"Error retrieving network information: {e}"

# Printing out results.
def print_system_info(system_info):
    for key, value in system_info.items():
        print(f"{key}: {value}")
 
def main():
    clear_screen()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    system_info = get_system_info()
    # Bug Issue with WSL
    print("*** For unknown reason with WSL it splits the network information with the system informaton in the middle. ***")
    print("*** you may need to scroll up to see all the network information.\n")
    print(f"System Information:  {timestamp}")
    print_system_info(system_info)
 
if __name__ == "__main__":
    print("Please wait while gathering information!")
    # Installing psutil library for Python
    subprocess.check_call([sys.executable, "-m", "pip", "install", "psutil"])
    import psutil
    main()
