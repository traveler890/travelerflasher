def flash_iso_to_drive(iso_path, drive_path):
    """
    Flash the ISO to the selected drive using raw Python I/O.
    WARNING: This will overwrite the target device completely.
    """
    try:
        # Try to unmount first (optional safety)
        import subprocess
        subprocess.run(["umount", drive_path], check=False)

        with open(iso_path, 'rb') as iso, open(drive_path, 'wb') as drive:
            total_bytes = 0
            while chunk := iso.read(4096):
                drive.write(chunk)
                total_bytes += len(chunk)

        # Optionally sync to ensure write completion
        subprocess.run(["sync"])

        print(f"✅ Flashed {total_bytes / 1e6:.2f} MB to {drive_path}")
        return True
    except Exception as e:
        print(f"❌ Flash error: {e}")
        return False
