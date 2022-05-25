# TO USE THE SPEED TEST! #
# To use the internet speed test you need to run 'pip install speedtest-cli' in a terminal. Then remove the hashtags from 'import speedtest' #
# and 'speed_test():' at the bottom. They have been disabled by default due to the needed installation. #

# *** It is recommended to edit the Site IP list to those that fit your needs *** #

import os
import socket
import datetime

# import speedtest

file = open("ping-log.txt", "w")
# Retrieve computer information #
def my_info():
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    print("\nComputer Name:       " + hostname)
    file.write("Computer Name:       " + hostname)
    print("Computer IP Address: " + IPAddr)
    file.write("\nComputer IP Address: " + IPAddr)
    file.write("\n ")


# Retrieve current time #
def time():
    current_time = datetime.datetime.now()
    print(f"\nBEGIN TESTING: {current_time} \n")
    file.write(f"\nBEGIN TESTING: {current_time} \n")
    file.write("\n")


# Testing Internet Speed #
def speed_test():
    st = speedtest.Speedtest()
    print("SPEED TEST")
    file.write("Speed Test\n")
    # Download speed #
    down = st.download() / 1000000
    downmbps = "{:.2f}".format(down)
    print(f"Download: {downmbps} mbps")
    file.write(f"Download: {downmbps} mbps\n")
    # Upload speed #
    up = st.upload() / 1000000
    upmbps = "{:.2f}".format(up)
    print(f"Upload: {upmbps} mbps\n")
    file.write(f"Upload: {upmbps} mbps\n")


# Testing site connections #
def ping_test():
    print("SITE CHECKING")
    file.write("\nSite Checking\n")
    # Enter IP address for testing in the list below #
    # Recommend to replace 192.168.1.1 with your internet gateway IP #
    ip_list = ["192.168.1.1", "1.1.1.1", "8.8.8.8"]
    for ip in ip_list:
        response = os.popen(f"ping {ip}").read()
        if "Received = 4" in response:
            print(f"{ip} UP")
            file.write(f"{ip} UP\n")
        else:
            print(f"{ip} ***DOWN***")
            file.write(f"{ip} ***DOWN***\n")


my_info()
time()
# speed_test()
ping_test()
print("\nTesting Complete!\n")
file.write("\nTesting Complete!")
file.close()
