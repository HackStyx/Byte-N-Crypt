import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QListWidget, QListWidgetItem
from PyQt5.QtGui import QFont, QPalette, QColor


class PasswordManager(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Password Manager")
        self.setGeometry(100, 100, 400, 400)

        self.passwords = {}

        self.setup_ui()
        self.load_passwords()

    def setup_ui(self):
        # Main layout
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_widget.setLayout(main_layout)

        # Password list
        password_list = QListWidget()
        main_layout.addWidget(password_list)

        # Password entry layout
        entry_layout = QVBoxLayout()
        entry_widget = QWidget()
        entry_widget.setStyleSheet("background-color: #E0EBF5; padding: 20px;")
        entry_widget.setLayout(entry_layout)
        main_layout.addWidget(entry_widget)

        label_font = QFont("Arial", 12)

        website_label = QLabel("Website:")
        website_label.setFont(label_font)
        entry_layout.addWidget(website_label)

        self.website_input = QLineEdit()
        self.website_input.setStyleSheet("background-color: white;")
        entry_layout.addWidget(self.website_input)

        username_label = QLabel("Username:")
        username_label.setFont(label_font)
        entry_layout.addWidget(username_label)

        self.username_input = QLineEdit()
        self.username_input.setStyleSheet("background-color: white;")
        entry_layout.addWidget(self.username_input)

        password_label = QLabel("Password:")
        password_label.setFont(label_font)
        entry_layout.addWidget(password_label)

        self.password_input = QLineEdit()
        self.password_input.setStyleSheet("background-color: white;")
        self.password_input.setEchoMode(QLineEdit.Password)
        entry_layout.addWidget(self.password_input)

        # Buttons layout
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        main_layout.addLayout(buttons_layout)

        add_button = QPushButton("Add")
        add_button.setStyleSheet("background-color: #4CAF50; color: white;")
        add_button.clicked.connect(self.add_password)
        buttons_layout.addWidget(add_button)

        view_button = QPushButton("View Password")
        view_button.setStyleSheet("background-color: #2196F3; color: white;")
        view_button.clicked.connect(self.view_password)
        buttons_layout.addWidget(view_button)

        edit_button = QPushButton("Edit Password")
        edit_button.setStyleSheet("background-color: #FF9800; color: white;")
        edit_button.clicked.connect(self.edit_password)
        buttons_layout.addWidget(edit_button)

        delete_button = QPushButton("Delete")
        delete_button.setStyleSheet("background-color: #F44336; color: white;")
        delete_button.clicked.connect(self.delete_password)
        buttons_layout.addWidget(delete_button)

        clear_button = QPushButton("Clear")
        clear_button.setStyleSheet("background-color: #9E9E9E; color: white;")
        clear_button.clicked.connect(self.clear_fields)
        buttons_layout.addWidget(clear_button)

    def add_password(self):
        website = self.website_input.text()
        username = self.username_input.text()
        password = self.password_input.text()

        if website and username and password:
            if website in self.passwords:
                reply = QMessageBox.question(
                    self,
                    "Website already exists",
                    f"The website '{website}' already exists. Do you want to overwrite the existing password?",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No,
                )

                if reply == QMessageBox.Yes:
                    self.passwords[website] = (username, password)
                    self.update_password_list()
                    self.save_passwords()
            else:
                self.passwords[website] = (username, password)
                self.update_password_list()
                self.save_passwords()
        else:
            QMessageBox.warning(self, "Missing Information", "Please enter website, username, and password.")

    def view_password(self):
        selected_items = self.centralWidget().layout().itemAt(0).widget().selectedItems()

        if selected_items:
            website = selected_items[0].text()
            username, password = self.passwords[website]
            QMessageBox.information(self, "View Password", f"Website: {website}\nUsername: {username}\nPassword: {password}")

    def edit_password(self):
        selected_items = self.centralWidget().layout().itemAt(0).widget().selectedItems()

        if selected_items:
            website = selected_items[0].text()
            username, password = self.passwords[website]
            self.website_input.setText(website)
            self.username_input.setText(username)
            self.password_input.setText(password)

    def delete_password(self):
        selected_items = self.centralWidget().layout().itemAt(0).widget().selectedItems()

        if selected_items:
            website = selected_items[0].text()
            reply = QMessageBox.question(
                self,
                "Delete Password",
                f"Are you sure you want to delete the password for '{website}'?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )

            if reply == QMessageBox.Yes:
                del self.passwords[website]
                self.update_password_list()
                self.save_passwords()

    def clear_fields(self):
        self.website_input.clear()
        self.username_input.clear()
        self.password_input.clear()

    def update_password_list(self):
        password_list = self.centralWidget().layout().itemAt(0).widget()
        password_list.clear()

        for website, (username, _) in self.passwords.items():
            item = QListWidgetItem(website)
            item.setToolTip(f"Username: {username}")
            password_list.addItem(item)

    def save_passwords(self):
        with open("passwords.txt", "w") as file:
            for website, (username, password) in self.passwords.items():
                file.write(f"{website},{username},{password}\n")

    def load_passwords(self):
        try:
            with open("passwords.txt", "r") as file:
                lines = file.readlines()

                for line in lines:
                    data = line.strip().split(",")
                    if len(data) == 3:
                        website, username, password = data
                        self.passwords[website] = (username, password)

            self.update_password_list()

        except FileNotFoundError:
            return


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PasswordManager()
    window.show()
    sys.exit(app.exec_())
