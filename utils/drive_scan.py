import psutil

def get_removable_drives():
    drives = []
    for part in psutil.disk_partitions():
        if 'removable' in part.opts or part.device.startswith('/dev/sd'):
            drives.append(part.device)
    return drives
