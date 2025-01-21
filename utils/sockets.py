import socket


def get_private_ip():
    try:
        # Connect to a non-existent external address (no data is sent)
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("192.168.0.1", 1))  # Local network example IP
            private_ip = s.getsockname()[0]
        return private_ip
    except Exception as e:
        return f"Error: Unable to retrieve private IP address: {e}"
