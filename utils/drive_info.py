import psutil
import platform

def get_removable_drives():
    """
    Returns a list of removable drive paths (e.g., /dev/sdb) with basic metadata.
    Filters out system drives like /dev/sda on Linux.
    """
    drives = []
    system_prefix = "/dev/sda"  # You can expand this for multi-disk setups

    partitions = psutil.disk_partitions(all=False)
    for p in partitions:
        device = p.device
        if device.startswith("/dev/sd") and not device.startswith(system_prefix):
            info = {
                "device": device,
                "mountpoint": p.mountpoint,
                "fstype": p.fstype,
                "is_removable": True
            }
            drives.append(info)
    return drives

def get_drive_label(path):
    """
    Returns volume label if available.
    """
    try:
        import subprocess
        result = subprocess.run(["lsblk", "-no", "LABEL", path], capture_output=True, text=True)
        return result.stdout.strip() or "Unnamed"
    except Exception:
        return "Unknown"

def get_drive_size(path):
    """
    Returns size of the given device in bytes.
    """
    try:
        usage = psutil.disk_usage(path)
        return usage.total
    except Exception:
        return 0

def is_drive_safe(path):
    """
    Determines if a drive is likely removable and safe to flash.
    """
    return path.startswith("/dev/sd") and not path.startswith("/dev/sda")
