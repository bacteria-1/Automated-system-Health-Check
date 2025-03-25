import psutil

# List of essential system processes to ignore
SYSTEM_PROCESSES = ["explorer.exe", "System", "svchost.exe", "csrss.exe", "wininit.exe"]

def list_processes():
    """List all running processes with PID, Name, CPU, and Memory Usage"""
    print(f"{'PID':<8}{'Process Name':<25}{'CPU (%)':<10}{'Memory (%)':<12}")
    print("="*55)
    
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            print(f"{proc.info['pid']:<8}{proc.info['name']:<25}{proc.info['cpu_percent']:<10.1f}{proc.info['memory_percent']:<12.1f}")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass  # Skip processes we can't access
    
    print("\n")

def is_unwanted(proc):
    """Check if a process is unwanted."""
    try:
        name = proc.name().lower()
        if name in SYSTEM_PROCESSES:
            return False  # Essential process, do not kill
        if proc.cpu_percent(interval=1) > 20:  # High CPU usage, likely needed
            return False
        if proc.memory_percent() > 10:  # High memory usage, likely needed
            return False
        return True  # Unwanted if none of the above conditions are met
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        return False  # Process is already gone or system-restricted

def kill_unwanted_processes():
    """Identify and kill unwanted processes."""
    print("Checking for unwanted processes...\n")
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        if is_unwanted(proc):
            try:
                print(f"Killing: {proc.info['name']} (PID: {proc.info['pid']}) - CPU: {proc.info['cpu_percent']}%, Mem: {proc.info['memory_percent']}%")
                proc.terminate()  # Try to terminate
            except psutil.NoSuchProcess:
                pass  # Process already exited
            except psutil.AccessDenied:
                print(f"Access Denied: {proc.info['name']} (PID: {proc.info['pid']})")

if __name__ == "__main__":
    print("Listing all processes with resource usage:\n")
    list_processes()
    
    # Kill unwanted processes
    kill_unwanted_processes()
