import socket
import queue

rx_queue = queue.Queue()


def udp_tx(message, port):
    # Create a UDP socket for broadcasting
    broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # Set the broadcast address
    broadcast_address = ('<broadcast>', port)  # all computers in this segment. LAN
    # broadcast_address = ('127.0.0.1', port)  # only my pc.

    try:
        # Send the broadcast message
        broadcast_socket.sendto(message.encode(), broadcast_address)
        # print(f"Broadcasted message to {broadcast_address}: {message}")
    except Exception as e:
        print(f"Error sending broadcast message: {str(e)}")
    finally:
        # Close the socket
        broadcast_socket.close()


def rx_udp():
    host_port = ('0.0.0.0', 15677)
    print("Start listening on", host_port)
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(host_port)  # Listen on all available interfaces
    while True:
        data, addr = udp_socket.recvfrom(1024)  # blocking wait for packet
        rx_queue.put(data) #.decode('utf-8', errors='ignore')
        # ip, port = addr
