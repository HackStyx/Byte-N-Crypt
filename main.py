import sys
import subprocess
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QSplashScreen, QWidget, QPushButton, QTextEdit, QVBoxLayout, QMessageBox, QGridLayout, QLabel
from PyQt5.QtGui import QFont, QPixmap, QPalette, QImage, QBrush
from PyQt5.QtCore import Qt, QTimer

class AnimationWindow:
    def __init__(self):
        self.app = QApplication(sys.argv)
        
        splash_pixmap = QPixmap(r"loading screen2.jpg")
        self.splash = QSplashScreen(splash_pixmap, Qt.WindowStaysOnTopHint)
        self.splash.setMask(splash_pixmap.mask())
        self.splash.show()

        # Simulate a loading delay (you can replace this with your actual loading process)
        QTimer.singleShot(1691, self.load_main_window)
        
        
    def load_main_window(self):
        self.splash.hide()
        
        self.window = QMainWindow()
        self.window.setWindowTitle("BYTE N CRYPT")
        self.window.setGeometry(100, 100, 1800, 1200)
      

        # Load your custom background image here
        background_image = QImage(r"homepage.png")
        background_image = background_image.scaled(1950, 1000)  # Scale to match window size
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(background_image))
        self.window.setPalette(palette)

        self.central_widget = QWidget()
        self.window.setCentralWidget(self.central_widget)

        self.create_main_window()

    def create_main_window(self):
        layout = QVBoxLayout()

        grid_layout = QGridLayout()
        community_post_button = QPushButton("Community Post")
        community_post_button.setFont(QFont("Arial", 18))
        community_post_button.clicked.connect(self.open_community_post)
        community_post_button.setStyleSheet("background-color: rgba(0, 0, 0, 0); color: white; border: 2px solid white; padding: 10px; text-align: center;")
        community_post_button.setCursor(Qt.PointingHandCursor)  
        community_post_button.setObjectName("community_button")
        grid_layout.addWidget(community_post_button, 0, 0, 1, 1, Qt.AlignRight)

        toolkit_button = QPushButton("Toolkit")
        toolkit_button.setFont(QFont("Arial", 18))
        toolkit_button.clicked.connect(self.open_toolkit)
        toolkit_button.setStyleSheet("background-color: rgba(0, 0, 0, 0); color: white; border: 2px solid white; padding: 10px; text-align: center;")
        toolkit_button.setCursor(Qt.PointingHandCursor)  # Change cursor on hover
        toolkit_button.setObjectName("toolkit_button")
        grid_layout.addWidget(toolkit_button, 1, 0, 1, 1, Qt.AlignRight)
        grid_layout.setSpacing(40)
        
        

        layout.addLayout(grid_layout)
        self.central_widget.setLayout(layout)
        
    
        self.window.closeEvent = self.confirm_quit
        
        self.window.show()
        
    def confirm_quit(self, event):
        confirm = QMessageBox.question(self.window, 'Exit Confirmation', 'Are you sure you want to quit?',
                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if confirm == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()



    def open_community_post(self):
        self.community_post_window = QMainWindow()
        self.community_post_window.setWindowTitle("Community Post(beta)")
        self.community_post_window.setGeometry(100, 100, 400, 300)

        central_widget = QWidget()
        self.community_post_window.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        name_entry = QTextEdit()
        layout.addWidget(name_entry)

        post_text = QTextEdit()
        layout.addWidget(post_text)

        create_button = QPushButton("Create Post")
        create_button.clicked.connect(self.create_post)
        layout.addWidget(create_button)

        read_button = QPushButton("Read Post")
        read_button.clicked.connect(self.read_post)
        layout.addWidget(read_button)

        clear_button = QPushButton("Clear Fields")
        clear_button.clicked.connect(self.clear_fields)
        layout.addWidget(clear_button)

        central_widget.setLayout(layout)

        self.community_post_window.show()

    def create_post(self):
        name = self.name_entry.toPlainText()  # Use toPlainText() to get text
        post = self.post_text.toPlainText()
        if name and post:
            self.save_post(name, post)
            QMessageBox.information(self.community_post_window, "Success", "Post created and saved successfully.")
            self.clear_fields()
        else:
            QMessageBox.critical(self.community_post_window, "Error", "Please enter both name and post.")

    def save_post(self, name, post):
        file_path = "community_posts.txt"
        with open(file_path, "a") as file:
            file.write(f"Name: {name}\n")
            file.write(f"Post: {post}\n\n")

    def read_post(self):
        file_path = "community_posts.txt"
        with open(file_path, "r") as file:
            self.post_text.setPlainText(file.read())  # Set text using setPlainText

    def clear_fields(self):
        self.name_entry.clear()
        self.post_text.clear()

    def open_toolkit(self):
        self.toolkit_window = QMainWindow()
        self.toolkit_window.setWindowTitle("Toolkit")
        self.toolkit_window.setGeometry(100, 100, 600, 400)
        
        background_image = QPixmap(r"toolkit back.jpg")
        background_image = background_image.scaled(1900, 900)
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(background_image))
        self.toolkit_window.setPalette(palette)
        
        central_widget = QWidget()
        self.toolkit_window.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        password_manager_button = QPushButton("Password Manager")
        password_manager_button.setFont(QFont("Arial", 14))
        password_manager_button.clicked.connect(self.password_manager)
        password_manager_button.setStyleSheet("background-color: #5733FF; color: white; border: none; padding: 10px; text-align: center;")
        password_manager_button.setCursor(Qt.PointingHandCursor)  # Change cursor on hover
        password_manager_button.setObjectName("Password Manager")
        layout.addWidget(password_manager_button)

        password_generator_button = QPushButton("Password Generator")
        password_generator_button.setFont(QFont("Arial", 14))
        password_generator_button.clicked.connect(self.password_generator)
        password_generator_button.setStyleSheet("background-color: #5733FF; color: white; border: none; padding: 10px; text-align: center;")
        password_generator_button.setCursor(Qt.PointingHandCursor)  # Change cursor on hover
        password_generator_button.setObjectName("Password Generator")
        layout.addWidget(password_generator_button)

        password_strength_checker_button = QPushButton("Password Strength Checker")
        password_strength_checker_button.setFont(QFont("Arial", 14))
        password_strength_checker_button.clicked.connect(self.password_strength_checker)
        password_strength_checker_button.setStyleSheet("background-color: #5733FF; color: white; border: none; padding: 10px; text-align: center;")
        password_strength_checker_button.setCursor(Qt.PointingHandCursor)  # Change cursor on hover
        password_strength_checker_button.setObjectName("Password Strength Checker")
        layout.addWidget(password_strength_checker_button)

        ip_lookup_button = QPushButton("IP Lookup")
        ip_lookup_button.setFont(QFont("Arial", 14))
        ip_lookup_button.clicked.connect(self.ip_look)
        ip_lookup_button.setStyleSheet("background-color: #5733FF; color: white; border: none; padding: 10px; text-align: center;")
        ip_lookup_button.setCursor(Qt.PointingHandCursor)  # Change cursor on hover
        ip_lookup_button.setObjectName("IP Lookup")
        layout.addWidget(ip_lookup_button)

        encryption_decryption_button = QPushButton("Encryption/Decryption")
        encryption_decryption_button.setFont(QFont("Arial", 14))
        encryption_decryption_button.clicked.connect(self.encryption_decryption)
        encryption_decryption_button.setStyleSheet("background-color: #5733FF; color: white; border: none; padding: 10px; text-align: center;")
        encryption_decryption_button.setCursor(Qt.PointingHandCursor)  # Change cursor on hover
        encryption_decryption_button.setObjectName("Encryption/Decryption")
        layout.addWidget(encryption_decryption_button)

        back_button = QPushButton("Back")
        back_button.setFont(QFont("Arial", 14))
        back_button.clicked.connect(self.toolkit_window.close)
        back_button.setStyleSheet("background-color: #000000; color: white; border: none; padding: 10px; text-align: center;")
        back_button.setCursor(Qt.PointingHandCursor)  # Change cursor on hover
        back_button.setObjectName("Back")
        layout.addWidget(back_button)

        central_widget.setLayout(layout)
        

        self.toolkit_window.show()

    def password_manager(self):
        subprocess.Popen(["python", r"password_manager.py"])

    def password_generator(self):
        subprocess.Popen(["python", r"password_generator"])

    def password_strength_checker(self):
        subprocess.Popen(["python", r"password_strength.py"])

    def ip_look(self):
        subprocess.Popen(["python", r"ip_lookup_latest.py"])

    def encryption_decryption(self):
        subprocess.Popen(["python", r"encry_decry.py"])

    def run(self):
        sys.exit(self.app.exec_())
        

if __name__ == "__main__":
    app = AnimationWindow()
    app.run()

