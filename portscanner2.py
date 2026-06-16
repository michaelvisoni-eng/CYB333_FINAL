import socket


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
        return result == 0

    except Exception as error:
        print(f"Error scanning port {port}: {error}")
        return False


def run_scan(target, start_port, end_port):
    print(f"\nScanning {target}...")
    print("-" * 30)

    open_ports = []

    for port in range(start_port, end_port + 1):
        if check_port(target, port):
            print(f"Port {port} is OPEN")
            open_ports.append(port)

    print("-" * 30)

    if open_ports:
        print("Open ports found:")
        print(open_ports)
    else:
        print("No open ports found.")


def main():
    print("Simple Port Scanner")
    print("Only scan systems you own or have permission to test.\n")

    target = input("Enter target IP address or hostname: ")

    start_port = int(input("Enter starting port: "))
    end_port = int(input("Enter ending port: "))

    run_scan(target, start_port, end_port)


if __name__ == "__main__":
    main()