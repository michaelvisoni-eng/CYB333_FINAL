import socket

TARGET = "127.0.0.1"
START_PORT = 20
END_PORT = 100

def check_port(host, port):
    try:
        # Create socket
        scanner = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Set timeout
        scanner.settimeout(1)

        # Attempt connection
        result = scanner.connect_ex((host, port))

        # Close socket
        scanner.close()

        # Port is open if connect_ex returns 0
        if result == 0:
            return True
        else:
            return False

    except Exception as error:
        print(f"Error scanning port {port}: {error}")
        return False

def run_scan():
    print(f"Scanning {TARGET}...")
    print("-" * 30)

    open_ports = []

    for port in range(START_PORT, END_PORT + 1):
        if check_port(TARGET, port):
            print(f"Port {port} is OPEN")
            open_ports.append(port)

    print("-" * 30)

    if open_ports:
        print("Open ports found:")
        print(open_ports)
    else:
        print("No open ports found.")

if __name__ == "__main__":
    run_scan()