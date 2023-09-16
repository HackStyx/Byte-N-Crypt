import sys
import requests
from PyQt5.QtWidgets import QApplication, QLabel, QLineEdit, QVBoxLayout, QWidget, QMessageBox, QScrollArea, QHBoxLayout, QPushButton
from PyQt5.QtGui import QFont, QIcon, QColor, QPalette
from PyQt5.QtCore import Qt


class IPLookupTool(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IP Lookup Tool")
        self.setWindowIcon(QIcon("icon.png"))  # Add an icon for the window
        self.layout = QVBoxLayout()
        self.init_ui()

    def init_ui(self):
        self.ip_label = QLabel("Enter IP Address:")
        self.ip_label.setFont(QFont("Arial", 12))
        self.ip_label.setAlignment(Qt.AlignCenter)

        self.ip_input = QLineEdit()
        self.ip_input.setFont(QFont("Arial", 12))
        self.ip_input.setAlignment(Qt.AlignCenter)
        self.ip_input.setPlaceholderText("Enter an IP address")

        # Styling the text box
        palette = self.ip_input.palette()
        palette.setColor(QPalette.Base, QColor("#FFFFFF"))  # Set background color
        palette.setColor(QPalette.Text, QColor("#000000"))  # Set text color
        palette.setColor(QPalette.PlaceholderText, QColor("#AAAAAA"))  # Set placeholder text color
        self.ip_input.setPalette(palette)
        self.ip_input.setStyleSheet(
            "QLineEdit { border: 1px solid #999999; border-radius: 5px; padding: 8px; }"
        )

        self.result_label = QLabel()
        self.result_label.setWordWrap(True)
        self.result_label.setFont(QFont("Arial", 12))
        self.result_label.setAlignment(Qt.AlignCenter)

        self.lookup_button_layout = QHBoxLayout()
        self.lookup_button_layout.setAlignment(Qt.AlignCenter)

        self.lookup_button = QPushButton("Lookup")
        self.lookup_button.setFont(QFont("Arial", 12))
        self.lookup_button.setStyleSheet(
            "QPushButton { background-color: #4CAF50; color: white; border-radius: 5px; padding: 10px; min-width: 100px; }"
            "QPushButton:hover { background-color: #45a049; }"
        )
        self.lookup_button.clicked.connect(self.lookup_ip)

        self.lookup_button_layout.addWidget(self.lookup_button)

        self.layout.addWidget(self.ip_label)
        self.layout.addWidget(self.ip_input)
        self.layout.addLayout(self.lookup_button_layout)
        self.layout.addWidget(self.result_label)

        widget = QWidget()
        widget.setLayout(self.layout)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(widget)

        self.setWindowFlag(Qt.WindowMinimizeButtonHint)  # Allow minimizing the window
        self.setWindowFlag(Qt.WindowMaximizeButtonHint)  # Allow maximizing the window
        self.resize(600, 400)  # Set the initial size of the window

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll_area)
        main_layout.setAlignment(Qt.AlignCenter)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Confirm Exit', 'Are you sure you want to exit?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def lookup_ip(self):
        ip_address = self.ip_input.text()
        if not ip_address:
            ip_address = requests.get('https://api.ipify.org').text  # Get user's own IP address

        try:
            response = requests.get(f"https://ipapi.co/{ip_address}/json/")
            data = response.json()
            if "error" in data:
                QMessageBox.critical(self, "Error", data["reason"])
            else:
                result = f"<b>IP:</b> {data['ip']}<br>" \
                         f"<b>City:</b> {data['city']}<br>" \
                         f"<b>Region:</b> {data['region']}<br>" \
                         f"<b>Country:</b> {data['country_name']}<br>" \
                         f"<b>Postal Code:</b> {data['postal']}<br>" \
                         f"<b>Latitude:</b> {data['latitude']}<br>" \
                         f"<b>Longitude:</b> {data['longitude']}<br>" \
                         f"<b>Service Provider:</b> {data['org']}<br>"  # Add service provider details
                self.result_label.setText(result)
        except requests.exceptions.RequestException:
            QMessageBox.critical(self, "Error", "An error occurred while fetching IP details.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = IPLookupTool()
    window.setStyleSheet(
        "background-color: #F2F2F2;"
        "QPushButton { font-size: 14px; }"
        "QLineEdit { padding: 8px; border-radius: 5px; border: 1px solid #ccc; }"
    )
    window.show()
    sys.exit(app.exec_())
