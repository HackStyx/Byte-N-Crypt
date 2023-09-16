import sys
import os
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QFileDialog,
    QMessageBox,
)
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtCore import Qt


class EncryptionDecryptionApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Encryption and Decryption")
        self.setGeometry(200, 200, 600, 400)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.title_label = QLabel("Encryption and Decryption", self)
        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        self.layout.addWidget(self.title_label, alignment=Qt.AlignCenter)

        self.selection_layout = QHBoxLayout()
        self.layout.addLayout(self.selection_layout)

        self.encryption_button = QPushButton("Encryption", self)
        self.encryption_button.setStyleSheet(
            """
            QPushButton {
                font-size: 16px;
                padding: 10px 20px;
                background-color: #6ac5fe;
                color: white;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #42a5f5;
            }
            """
        )
        self.encryption_button.clicked.connect(self.select_encryption)
        self.selection_layout.addWidget(self.encryption_button)

        self.decryption_button = QPushButton("Decryption", self)
        self.decryption_button.setStyleSheet(
            """
            QPushButton {
                font-size: 16px;
                padding: 10px 20px;
                background-color: #6ac5fe;
                color: white;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #42a5f5;
            }
            """
        )
        self.decryption_button.clicked.connect(self.select_decryption)
        self.selection_layout.addWidget(self.decryption_button)

        self.selected_file = ""
        self.current_page = None

        self.set_palette()

    def set_palette(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(240, 240, 240))
        palette.setColor(QPalette.Button, QColor(200, 200, 200))
        palette.setColor(QPalette.ButtonText, QColor(40, 40, 40))
        palette.setColor(QPalette.Base, QColor(255, 255, 255))
        palette.setColor(QPalette.Text, QColor(40, 40, 40))
        self.setPalette(palette)

    def select_encryption(self):
        self.clear_layout()
        self.create_encryption_window()

    def select_decryption(self):
        self.clear_layout()
        self.create_decryption_window()

    def create_encryption_window(self):
        self.current_page = "Encryption"

        self.file_layout = QHBoxLayout()
        self.layout.addLayout(self.file_layout)

        self.file_label = QLabel("File:", self)
        self.file_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        self.file_layout.addWidget(self.file_label)

        self.file_entry = QLineEdit(self)
        self.file_entry.setReadOnly(True)
        self.file_layout.addWidget(self.file_entry)

        self.browse_button = QPushButton("Browse", self)
        self.browse_button.setStyleSheet(
            """
            QPushButton {
                font-size: 12px;
                padding: 5px 10px;
                background-color: #42a5f5;
                color: white;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #2196f3;
            }
            """
        )
        self.browse_button.clicked.connect(self.browse_file)
        self.file_layout.addWidget(self.browse_button)

        self.encryption_key_label = QLabel("Encryption Key:", self)
        self.encryption_key_label.setStyleSheet("font-size: 14px; font-weight: bold; margin-top: 20px;")
        self.layout.addWidget(self.encryption_key_label)

        self.encryption_key_text = QTextEdit(self)
        self.encryption_key_text.setReadOnly(True)
        self.layout.addWidget(self.encryption_key_text)

        self.generate_key_button = QPushButton("Generate Encryption Key", self)
        self.generate_key_button.setStyleSheet(
            """
            QPushButton {
                font-size: 12px;
                padding: 5px 10px;
                background-color: #42a5f5;
                color: white;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #2196f3;
            }
            """
        )
        self.generate_key_button.clicked.connect(self.generate_encryption_key)
        self.layout.addWidget(self.generate_key_button)

        self.encrypt_button = QPushButton("Encrypt", self)
        self.encrypt_button.setStyleSheet(
            """
            QPushButton {
                font-size: 14px;
                padding: 10px 20px;
                background-color: #4caf50;
                color: white;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #43a047;
            }
            """
        )
        self.encrypt_button.clicked.connect(self.encrypt_file)
        self.layout.addWidget(self.encrypt_button)

        self.back_button = QPushButton("Back", self)
        self.back_button.setStyleSheet(
            """
            QPushButton {
                font-size: 14px;
                padding: 10px 20px;
                background-color: #f44336;
                color: white;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #e53935;
            }
            """
        )
        self.back_button.clicked.connect(self.go_to_main_page)
        self.layout.addWidget(self.back_button)

    def create_decryption_window(self):
        self.current_page = "Decryption"

        self.file_layout = QHBoxLayout()
        self.layout.addLayout(self.file_layout)

        self.file_label = QLabel("File:", self)
        self.file_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        self.file_layout.addWidget(self.file_label)

        self.file_entry = QLineEdit(self)
        self.file_entry.setReadOnly(True)
        self.file_layout.addWidget(self.file_entry)

        self.browse_button = QPushButton("Browse", self)
        self.browse_button.setStyleSheet(
            """
            QPushButton {
                font-size: 12px;
                padding: 5px 10px;
                background-color: #42a5f5;
                color: white;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #2196f3;
            }
            """
        )
        self.browse_button.clicked.connect(self.browse_file)
        self.file_layout.addWidget(self.browse_button)

        self.decryption_key_label = QLabel("Decryption Key:", self)
        self.decryption_key_label.setStyleSheet("font-size: 14px; font-weight: bold; margin-top: 20px;")
        self.layout.addWidget(self.decryption_key_label)

        self.decryption_key_text = QTextEdit(self)
        self.layout.addWidget(self.decryption_key_text)

        self.decrypt_button = QPushButton("Decrypt", self)
        self.decrypt_button.setStyleSheet(
            """
            QPushButton {
                font-size: 14px;
                padding: 10px 20px;
                background-color: #f44336;
                color: white;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #e53935;
            }
            """
        )
        self.decrypt_button.clicked.connect(self.decrypt_file)
        self.layout.addWidget(self.decrypt_button)

        self.back_button = QPushButton("Back", self)
        self.back_button.setStyleSheet(
            """
            QPushButton {
                font-size: 14px;
                padding: 10px 20px;
                background-color: #f44336;
                color: white;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #e53935;
            }
            """
        )
        self.back_button.clicked.connect(self.go_to_main_page)
        self.layout.addWidget(self.back_button)

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*.*)")
        if file_path:
            self.selected_file = file_path
            self.file_entry.setText(self.selected_file)

    def generate_encryption_key(self):
        encryption_key = os.urandom(16).hex()
        self.encryption_key_text.setText(encryption_key)

    def encrypt_file(self):
        file_path = self.selected_file
        encryption_key = self.encryption_key_text.toPlainText().strip()

        if file_path and encryption_key:
            try:
                with open(file_path, "rb+") as file:
                    original_data = file.read()

                    encrypted_data = self.xor_encrypt_decrypt(original_data, encryption_key)

                    # Go back to the beginning of the file
                    file.seek(0)
                    file.write(encrypted_data)

                    # Truncate the file to the size of the encrypted data
                    file.truncate(len(encrypted_data))

                QMessageBox.information(self, "Encryption Successful", "File encrypted successfully.")
            except Exception as e:
                QMessageBox.critical(self, "Encryption Error", f"Failed to encrypt file: {e}")
        else:
            QMessageBox.warning(self, "Missing Information", "Please enter the file path and encryption key.")

    def decrypt_file(self):
        file_path = self.selected_file
        decryption_key = self.decryption_key_text.toPlainText().strip()

        if file_path and decryption_key:
            try:
                with open(file_path, "rb+") as file:
                    encrypted_data = file.read()

                    decrypted_data = self.xor_encrypt_decrypt(encrypted_data, decryption_key)

                    # Go back to the beginning of the file
                    file.seek(0)
                    file.write(decrypted_data)

                    # Truncate the file to the size of the decrypted data
                    file.truncate(len(decrypted_data))

                QMessageBox.information(self, "Decryption Successful", "File decrypted successfully.")
            except Exception as e:
                QMessageBox.critical(self, "Decryption Error", f"Failed to decrypt file: {e}")
        else:
            QMessageBox.warning(self, "Missing Information", "Please enter the file path and decryption key.")

    def xor_encrypt_decrypt(self, data, key):
        key_length = len(key)
        key_stream = [ord(key[i % key_length]) for i in range(len(data))]
        return bytes([data[i] ^ key_stream[i] for i in range(len(data))])

    def go_to_main_page(self):
        self.clear_layout()
        self.create_main_page()

    def create_main_page(self):
        self.current_page = None

        self.title_label = QLabel("Encryption and Decryption", self)
        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        self.layout.addWidget(self.title_label, alignment=Qt.AlignCenter)

        self.selection_layout = QHBoxLayout()
        self.layout.addLayout(self.selection_layout)

        self.encryption_button = QPushButton("Encryption", self)
        self.encryption_button.setStyleSheet(
            """
            QPushButton {
                font-size: 16px;
                padding: 10px 20px;
                background-color: #6ac5fe;
                color: white;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #42a5f5;
            }
            """
        )
        self.encryption_button.clicked.connect(self.select_encryption)
        self.selection_layout.addWidget(self.encryption_button)

        self.decryption_button = QPushButton("Decryption", self)
        self.decryption_button.setStyleSheet(
            """
            QPushButton {
                font-size: 16px;
                padding: 10px 20px;
                background-color: #6ac5fe;
                color: white;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #42a5f5;
            }
            """
        )
        self.decryption_button.clicked.connect(self.select_decryption)
        self.selection_layout.addWidget(self.decryption_button)

    def clear_layout(self):
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Set the font globally for the application
    font = QFont("Arial", 12)
    app.setFont(font)

    window = EncryptionDecryptionApp()
    window.show()
    sys.exit(app.exec_())
