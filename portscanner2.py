import socket
import datetime
import json
import threading


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

def get_service(port):
    try:
        return socket.getservbyport(port)
    except OSError:
        return "Unknown"
    
def get_banner(host, port):
    try:
        scanner = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        scanner.settimeout(2)

        scanner.connect((host, port))

        banner = scanner.recv(1024).decode(errors="ignore").strip()

        scanner.close()

        return banner if banner else "No banner returned"

    except Exception:
        return "Banner unavailable"

def save_text_report(target, start_port, end_port, open_ports):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = "scan_report.txt"

    with open(filename, "w") as report:
        report.write("Simple Port Scanner Report\n")
        report.write("=" * 30 + "\n")
        report.write(f"Target: {target}\n")
        report.write(f"Port Range: {start_port}-{end_port}\n")
        report.write(f"Scan Time: {timestamp}\n")
        report.write(f"Open Ports Found: {len(open_ports)}\n")
        report.write("=" * 30 + "\n\n")

        if open_ports:
            report.write("Open Ports:\n")

            for item in open_ports:
                report.write(f"Port {item['port']}: {item['service']}\n")
        else:
            report.write("No open ports were found.\n")

    print(f"\nText report saved as {filename}")

def save_json_report(target, start_port, end_port, open_ports):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = "scan_report.json"

    report_data = {
        "target": target,
        "port_range": f"{start_port}-{end_port}",
        "scan_time": timestamp,
        "open_ports_found": len(open_ports),
        "open_ports": open_ports
    }

    with open(filename, "w") as report:
        json.dump(report_data, report, indent=4)

    print(f"JSON report saved as {filename}")

def scan_port(target, port, open_ports):
    if check_port(target, port):
        service = get_service(port)

        banner = get_banner(target, port)

        print(f"Port {port} is OPEN ({service})")
        print(f"Banner: {banner}")

        open_ports.append({
            "port": port,
            "service": service,
            "banner": banner
        })

def run_scan(target, start_port, end_port):
    print(f"\nScanning {target}...")
    print("-" * 30)

    open_ports = []

    threads = []

    for port in range(start_port, end_port + 1):
        thread = threading.Thread(
            target=scan_port,
            args=(target, port, open_ports)
        )

        threads.append(thread)

        thread.start()

    for thread in threads:
        thread.join()

    print("-" * 30)

    if open_ports:
        print("Open ports found:")
        print(open_ports)
    else:
        print("No open ports found.")

    save_text_report(target, start_port, end_port, open_ports)
    save_json_report(target, start_port, end_port, open_ports)

def main():
    print("Simple Port Scanner")
    print("Only scan systems you own or have permission to test.\n")

    target = input("Enter target IP address or hostname: ")

    start_port = int(input("Enter starting port: "))
    end_port = int(input("Enter ending port: "))

    run_scan(target, start_port, end_port)


if __name__ == "__main__":
    main()