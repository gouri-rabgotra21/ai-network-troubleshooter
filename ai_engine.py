import subprocess

def ping_device(ip):
    try:
        output = subprocess.check_output(
            ["ping", ip, "-n", "1"],
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )
        return output
    except subprocess.CalledProcessError as e:
        return e.output

def troubleshoot_ping(ping_results):
    issues = []
    for device, result in ping_results.items():
        if "TTL expired in transit" in result:
            issues.append(f"{device} has routing issues. 🛰️ Check routing tables or default gateway settings.")
        elif "Request timed out" in result or "Destination host unreachable" in result:
            if "PC" in device:
                issues.append(f"{device} is unreachable. 🧩 Check if it's powered on and properly connected.")
            elif "Router" in device:
                issues.append(f"{device} is down. 📡 Verify router is powered and interfaces are configured.")
            elif "Switch" in device:
                issues.append(f"{device} might be disconnected. 🧷 Inspect switch cables or VLAN settings.")
            else:
                issues.append(f"{device} is not responding. 🔍 Check IP configuration and physical links.")
    return issues
