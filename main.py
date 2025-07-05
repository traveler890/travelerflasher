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

