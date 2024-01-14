import sys
import re
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtCore import Qt


class PasswordStrengthChecker(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Password Strength Checker")
        self.setGeometry(0, 0, 600, 400)

        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        layout = QVBoxLayout(main_widget)
        layout.setAlignment(Qt.AlignCenter)

        self.password_label = QLabel("Enter Password:", self)
        self.password_label.setFont(QFont("Arial", 12))
        layout.addWidget(self.password_label)

        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedWidth(300)
        layout.addWidget(self.password_input)

        self.view_button = QPushButton("Show", self)
        self.view_button.setFixedWidth(60)
        self.view_button.setStyleSheet("QPushButton { background-color: #F2F2F2; border: 1px solid #DADADA; border-radius: 5px; padding: 5px; }"
                                        "QPushButton:hover { background-color: #E6E6E6; }"
                                        "QPushButton:pressed { background-color: #DADADA; }")
        layout.addWidget(self.view_button)

        self.check_button = QPushButton("Check Strength", self)
        self.check_button.setFixedWidth(150)
        self.check_button.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; border-radius: 5px; padding: 5px; }"
                                        "QPushButton:hover { background-color: #45A049; }"
                                        "QPushButton:pressed { background-color: #3C893D; }")
        layout.addWidget(self.check_button)

        self.result_label = QLabel(self)
        self.result_label.setFont(QFont("Arial", 12))
        layout.addWidget(self.result_label)

        self.check_button.clicked.connect(self.check_password_strength)
        self.view_button.clicked.connect(self.view_password)

        self.password_input.returnPressed.connect(self.check_button.click)

    def check_password_strength(self):
        password = self.password_input.text()
        strength = self.calculate_password_strength(password)
        if strength == 0:
            self.result_label.setText("Weak Password")
            self.result_label.setStyleSheet("color: red")
        elif strength == 1:
            self.result_label.setText("Medium Password")
            self.result_label.setStyleSheet("color: orange")
        else:
            self.result_label.setText("Strong Password")
            self.result_label.setStyleSheet("color: green")

    def view_password(self):
        if self.password_input.echoMode() == QLineEdit.Password:
            self.password_input.setEchoMode(QLineEdit.Normal)
            self.view_button.setText("Hide")
        else:
            self.password_input.setEchoMode(QLineEdit.Password)
            self.view_button.setText("Show")

    @staticmethod
    def calculate_password_strength(password):

        length = len(password)

        has_lowercase = any(char.islower() for char in password)
        has_uppercase = any(char.isupper() for char in password)
        has_digit = any(char.isdigit() for char in password)
        has_special_char = re.search(r'[!@#$%^&*(),.?":{}|<>]', password) is not None

        complexity = 0

        complexity += has_lowercase
        complexity += has_uppercase
        complexity += has_digit
        complexity += has_special_char

        if length >= 8:
            complexity += 1
        if length >= 12:
            complexity += 1
        if length >= 16:
            complexity += 1

        if complexity < 3:
            return 0  # Weak password
        elif complexity < 5:
            return 1  # Medium password
        else:
            return 2  # Strong password


    def closeEvent(self, event):
        confirm_exit = self.confirmExit()
        if confirm_exit:
            event.accept()
        else:
            event.ignore()

    @staticmethod
    def confirmExit():
        choice = QMessageBox.question(None, "Exit Confirmation",
                                      "Are you sure you want to exit?", 
                                      QMessageBox.Yes | QMessageBox.No)
        return choice == QMessageBox.Yes


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PasswordStrengthChecker()
    
    # Setting the background color
    palette = window.palette()
    palette.setColor(QPalette.Window, QColor(240, 240, 240))
    window.setPalette(palette)
    
    window.show()
    sys.exit(app.exec_())
 