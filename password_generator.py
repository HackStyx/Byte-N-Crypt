import sys
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QLineEdit, QMessageBox, QCheckBox, QVBoxLayout, QHBoxLayout, QWidget
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class PasswordGenerator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Password Generator")
        self.setGeometry(100, 100, 400, 300)

        # Create the central widget and layout
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setAlignment(Qt.AlignCenter)

        # Create the length label and entry field
        self.length_label = QLabel("Password Length:", self)
        self.length_label.setFont(QFont("Arial", 10, QFont.Bold))
        self.layout.addWidget(self.length_label)
        self.length_entry = QLineEdit(self)

        # Create the options checkboxes
        self.uppercase_checkbox = QCheckBox("Include Uppercase Letters", self)
        self.lowercase_checkbox = QCheckBox("Include Lowercase Letters", self)
        self.digits_checkbox = QCheckBox("Include Digits", self)
        self.special_chars_checkbox = QCheckBox("Include Special Characters", self)

        # Create the generate button
        self.generate_button = QPushButton("Generate Password", self)
        self.generate_button.clicked.connect(self.generate_password)
        self.generate_button.setStyleSheet("background-color: #4CAF50; color: white;")

        # Create the password label and entry field
        self.password_label = QLabel("Generated Password:", self)
        self.password_entry = QLineEdit(self)
        self.password_entry.setEchoMode(QLineEdit.Password)
        self.password_entry.setStyleSheet("background-color: #F0F0F0;")

        # Create the save and view buttons
        self.save_button = QPushButton("Save Password", self)
        self.save_button.clicked.connect(self.save_password)
        self.save_button.setStyleSheet("background-color: #2196F3; color: white;")
        self.view_button = QPushButton("View Password", self)
        self.view_button.clicked.connect(self.view_password)
        self.view_button.setStyleSheet("background-color: #9C27B0; color: white;")

        # Create a horizontal layout for the buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.view_button)

        # Add widgets to the main layout
        self.layout.addWidget(self.length_entry)
        self.layout.addWidget(self.uppercase_checkbox)
        self.layout.addWidget(self.lowercase_checkbox)
        self.layout.addWidget(self.digits_checkbox)
        self.layout.addWidget(self.special_chars_checkbox)
        self.layout.addWidget(self.generate_button)
        self.layout.addWidget(self.password_label)
        self.layout.addWidget(self.password_entry)
        self.layout.addLayout(button_layout)

        # Set the main layout for the central widget
        self.central_widget.setLayout(self.layout)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, "Quit", "Are you sure you want to quit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def generate_password(self):
        length_text = self.length_entry.text()

        if not length_text.isdigit():
            QMessageBox.warning(self, "Warning", "Password length should be a valid positive integer.")
            return

        length = int(length_text)

        if length <= 0:
            QMessageBox.warning(self, "Warning", "Password length should be greater than 0.")
            return

        use_uppercase = self.uppercase_checkbox.isChecked()
        use_lowercase = self.lowercase_checkbox.isChecked()
        use_digits = self.digits_checkbox.isChecked()
        use_special_chars = self.special_chars_checkbox.isChecked()

        characters = ""
        if use_uppercase:
            characters += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if use_lowercase:
            characters += "abcdefghijklmnopqrstuvwxyz"
        if use_digits:
            characters += "0123456789"
        if use_special_chars:
            characters += "!@#$%^&*()_+=-{}[]|:;<>,.?/~"

        if not characters:
            QMessageBox.warning(self, "Warning", "Please select at least one character type.")
            return

        password = "".join(random.choice(characters) for _ in range(length))

        self.password_entry.setText(password)

    def save_password(self):
        password = self.password_entry.text()

        if len(password) == 0:
            QMessageBox.warning(self, "Warning", "No password generated.")
            return

        file_path = r"C:\toolkit\pass.txt.txt"

        try:
            with open(file_path, "w") as file:
                file.write(password)
            QMessageBox.information(self, "Success", "Password saved successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def view_password(self):
        file_path = r"C:\toolkit\pass.txt.txt"

        try:
            with open(file_path, "r") as file:
                password = file.read()
            QMessageBox.information(self, "Password", password)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


app = QApplication(sys.argv)
window = PasswordGenerator()
window.show()
sys.exit(app.exec_())
