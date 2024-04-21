import socket

def send_message_to_esp32(message, esp32_ip='192.168.1.84', esp32_port=12345):
    """
    Send a message to an ESP32 device over TCP/IP.

    Args:
    - message: The message to be sent.
    - esp32_ip (optional): The IP address of the ESP32 device. Default is '192.168.1.84'.
    - esp32_port (optional): The port number on which the ESP32 device is listening. Default is 12345.
    """
    # Create a TCP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the ESP32
        sock.connect((esp32_ip, esp32_port))

        # Send the message
        sock.sendall(message.encode())

        print("Message sent successfully!")

    except Exception as e:
        print("Error:", e)

    finally:
        # Close the socket
        sock.close()
