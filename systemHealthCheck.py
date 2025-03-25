import psutil
import platform
import socket
import shutil
import time

def get_system_info():
    system_info = {
        "OS": platform.system(),
        "OS Version": platform.version(),
        "Architecture": platform.architecture()[0],
        "Processor": platform.processor(),
        "Hostname": socket.gethostname(),
        "IP Address": socket.gethostbyname(socket.gethostname())
    }
    return system_info

def get_cpu_usage():
    return psutil.cpu_percent(interval=1)

def get_memory_usage():
    mem = psutil.virtual_memory()
    return {
        "Total": mem.total,
        "Available": mem.available,
        "Used": mem.used,
        "Percentage": mem.percent
    }

def get_disk_usage():
    disk = shutil.disk_usage("/")
    return {
        "Total": disk.total,
        "Used": disk.used,
        "Free": disk.free,
        "Percentage": (disk.used / disk.total) * 100
    }

def get_network_info():
    net_io = psutil.net_io_counters()
    return {
        "Bytes Sent": net_io.bytes_sent,
        "Bytes Received": net_io.bytes_recv
    }

def get_user_processes(username):
    user_processes = []
    for proc in psutil.process_iter(['pid', 'name', 'username']):
        if proc.info['username'] == username:
            user_processes.append(proc.info)
    return user_processes

def generate_report():
    report = {
        "System Info": get_system_info(),
        "CPU Usage (%)": get_cpu_usage(),
        "Memory Usage": get_memory_usage(),
        "Disk Usage": get_disk_usage(),
        "Network Usage": get_network_info(),
        "User Processes": get_user_processes("ADMN\\bakteriam")
    }
    return report

def print_report(report):
    print("\nSystem Health Report:")
    for key, value in report.items():
        if key == "User Processes":
            print("\nUser Processes:")
            print("{:<10} {:<25} {:<20}".format("PID", "Process Name", "Username"))
            print("-" * 60)
            for proc in value:
                print("{:<10} {:<25} {:<20}".format(proc['pid'], proc['name'], proc['username']))
        else:
            print(f"{key}: {value}")
    print("-" * 50)

def main():
    while True:
        health_report = generate_report()
        print_report(health_report)
        time.sleep(10)  # Check every 10 seconds

if __name__ == "__main__":
    main()
