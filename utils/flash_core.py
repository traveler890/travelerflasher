import subprocess

def flash_iso_to_drive(iso_path, drive_path):
    try:
        subprocess.run(["umount", drive_path], check=False)
        with open(iso_path, 'rb') as iso, open(drive_path, 'wb') as drive:
            while chunk := iso.read(4096):
                drive.write(chunk)
        return True
    except Exception as e:
        print(f"Flash error: {e}")
        return False
