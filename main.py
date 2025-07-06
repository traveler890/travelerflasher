from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtWidgets import QProgressBar

import os
import sys
import requests
import psutil
from utils.iso_tools import sha256_file
from utils.flash_core import flash_iso_to_drive
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QPushButton, QComboBox, QMessageBox
)

from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtWidgets import QProgressBar

class TravelerFlasher(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TravelerFlasher")
        self.setFixedSize(400, 300)

        layout = QVBoxLayout()

        self.intro_label = QLabel("🚀 Welcome to TravelerFlasher! Choose a TravelerOS version and target drive.")
        layout.addWidget(self.intro_label)

        self.version_picker = QComboBox()
        self.version_picker.addItem("Fetching available versions...")
        layout.addWidget(self.version_picker)

        self.drive_picker = QComboBox()
        self.drive_picker.addItem("Detecting drives...")
        layout.addWidget(self.drive_picker)

        self.populate_drives()
        self.drive_picker.currentIndexChanged.connect(self.update_selected_drive)

        self.flash_button = QPushButton("Flash TravelerOS")
        self.flash_button.clicked.connect(self.flash_iso)
        layout.addWidget(self.flash_button)

        self.status_label = QLabel("Status: Awaiting input.")
        layout.addWidget(self.status_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        # App icon (optional for window & PyInstaller)
        self.setWindowIcon(QIcon("assets/traveler-logo.png"))

        # Logo banner
        banner = QLabel()
        pixmap = QPixmap("assets/traveler-logo.png")
        banner.setPixmap(pixmap.scaledToHeight(64))
        layout.addWidget(banner)

        # Tagline
        tagline = QLabel("<i>Flash fast. Travel far.</i>")
        layout.addWidget(tagline)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        
        self.setLayout(layout)
        self.drive_path = None
        self.fetch_versions()

    def populate_drives(self):
        self.drive_picker.clear()
        drives = get_removable_drives()
        if drives:
            for d in drives:
                self.drive_picker.addItem(d)
            self.status_label.setText("✅ Removable drives detected.")
        else:
            self.drive_picker.addItem("No removable drives found")
            self.status_label.setText("⚠️ No drives available.")

    def update_selected_drive(self):
        self.drive_path = self.drive_picker.currentText()

 def download_iso(self, url, output_path):
    self.status_label.setText("⬇️ Downloading TravelerOS ISO...")
    self.progress_bar.setValue(0)
    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            total_size = int(r.headers.get('content-length', 0))
            downloaded = 0

            with open(output_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        percent = int(downloaded * 100 / total_size)
                        self.status_label.setText(f"📦 Downloading... {percent}%")
                        self.progress_bar.setValue(percent)
        self.progress_bar.setValue(100)
        return True
    except Exception as e:
        self.status_label.setText(f"❌ Download error: {e}")
        self.progress_bar.setValue(0)
        return False

    def flash_iso(self):
        if not self.drive_path:
            QMessageBox.warning(self, "No Drive", "Please select a USB drive first.")
            return

        index = self.version_picker.currentIndex()
        if index < 0 or index >= len(self.version_data):
            QMessageBox.warning(self, "Invalid Selection", "Please select a valid TravelerOS version.")
            return

        release = self.version_data[index]
        iso_url = release.get("url")
        iso_hash = release.get("sha256")
        iso_name = release.get("name")
        output_iso = os.path.join(os.getcwd(), "TravelerOS-temp.iso")

        if not self.download_iso(iso_url, output_iso):
            return

        actual_hash = sha256_file(output_iso)
        if actual_hash != iso_hash:
            QMessageBox.warning(self, "Hash Mismatch", "ISO checksum does not match! Aborting.")
            self.status_label.setText("❌ Hash mismatch.")
            return
        self.status_label.setText("✅ ISO verified.")

        success = flash_iso_to_drive(output_iso, self.drive_path)
        if success:
            self.status_label.setText("✅ TravelerOS flashed successfully!")
        else:
            self.status_label.setText("❌ Flashing failed.")
