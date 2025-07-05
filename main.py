# main.py

import sys
import requests
import psutil
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QPushButton, QFileDialog, QComboBox, QMessageBox
)

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

        self.drive_button = QPushButton("Select USB Drive")
        self.drive_button.clicked.connect(self.choose_drive)
        layout.addWidget(self.drive_button)

        self.flash_button = QPushButton("Flash TravelerOS")
        self.flash_button.clicked.connect(self.flash_iso)
        layout.addWidget(self.flash_button)

        self.status_label = QLabel("Status: Awaiting input.")
        layout.addWidget(self.status_label)

        self.setLayout(layout)
        self.drive_path = None
        self.fetch_versions()

    def fetch_versions(self):
        try:
            # Replace with actual API or GitHub raw JSON URL
            response = requests.get("https://your-repo.com/traveler-versions.json")
            versions = response.json().get("releases", [])
            self.version_picker.clear()
            for v in versions:
                self.version_picker.addItem(v["name"])
        except Exception as e:
            self.version_picker.clear()
            self.version_picker.addItem("Version fetch failed")
            self.status_label.setText(f"Error fetching versions: {e}")

    def choose_drive(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.Directory)
        if file_dialog.exec():
            self.drive_path = file_dialog.selectedFiles()[0]
            self.status_label.setText(f"Selected drive: {self.drive_path}")
            QMessageBox.information(self, "Drive Selected", f"Target device: {self.drive_path}")

    def flash_iso(self):
        if not self.drive_path:
            QMessageBox.warning(self, "No Drive", "Please select a USB drive first.")
            return
        selected_version = self.version_picker.currentText()
        QMessageBox.information(self, "Coming Soon", f"Flashing TravelerOS version '{selected_version}' to '{self.drive_path}' is under construction.")
        self.status_label.setText("🚧 Flashing logic is being built...")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TravelerFlasher()
    window.show()
    sys.exit(app.exec())
