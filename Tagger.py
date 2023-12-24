"""

"""
import queue
import socket

# Import the required modules
import nicegui as ng
from nicegui import ui
import pandas as pd
import threading
import time

# Create a sample Pandas DataFrame
test_data = {
    'Name': ['Alice', 'Bob', 'Charlie', 'David'],
    'Age': [25, 30, 35, 40],
    'City': ['New York', 'Los Angeles', 'Chicago', 'Houston']
}

rx_queue = queue.Queue()
gun_info = pd.DataFrame(test_data)

table = ui.table(
    columns=[{'field': col} for col in gun_info.columns],
    rows=gun_info.to_dict('records'),
)

age = 103


def rx_UDP():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(('0.0.0.0', 15677))  # Listen on all available interfaces
    while True:
        data, addr = udp_socket.recvfrom(1024)  # blocking wait for packet
        rx_queue.put(data.decode('utf-8', errors='ignore'))
        ip, port = addr

def process_UDP():
    global age, gun_info
    while True:
        while not rx_queue.empty():
            new_row = {'Name': 'Eve', 'Age': age, 'City': 'Miami'}
            age += 1
            gun_info = pd.concat([gun_info, pd.DataFrame([new_row])], ignore_index=True)
            table.update_rows(gun_info.to_dict('records'))
        time.sleep(0.1)  # Sleep for 100ms

# Start the threads
UDP_RX = threading.Thread(target=rx_UDP)
UDP_RX.daemon = True
UDP_RX.start()

packet_proces = threading.Thread(target=process_UDP)
packet_proces.daemon = True
packet_proces.start()

# Display the DataFrame using NiceGUI
ui.run(port=9000)
