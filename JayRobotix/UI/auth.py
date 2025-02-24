import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, 
    QVBoxLayout, QMessageBox, QStackedWidget
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

API_URL = "http://127.0.0.1:8000"

class StyledWindow(QWidget):
    def set_styling(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #2c3e50;
                color: white;
                font-size: 14px;
            }
            QLabel {
                font-size: 16px;
                font-weight: bold;
            }
            QLineEdit {
                background-color: white;
                color: black;
                border: 2px solid #34495e;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton {
                background-color: #1abc9c;
                color: white;
                border-radius: 5px;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #16a085;
            }
        """)

class LoginWindow(StyledWindow):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.initUI()
        self.set_styling()

    def initUI(self):
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 350, 250)

        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit(self)

        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton("Login", self)
        self.login_button.clicked.connect(self.login)

        self.register_button = QPushButton("Go to Register", self)
        self.register_button.clicked.connect(self.show_register)

        layout = QVBoxLayout()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.register_button)
        layout.setAlignment(Qt.AlignCenter)
        
        self.setLayout(layout)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, "Error", "All fields are required")
            return

        data = {'username': username, 'password': password}
        response = requests.post(f"{API_URL}/login/", json=data)

        if response.status_code == 200:
            QMessageBox.information(self, "Success", "Login successful!")
            self.stacked_widget.setCurrentIndex(2)
        else:
            QMessageBox.warning(self, "Error", response.json().get("error", "Login failed"))

    def show_register(self):
        self.stacked_widget.setCurrentIndex(1)

class RegisterWindow(StyledWindow):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.initUI()
        self.set_styling()

    def initUI(self):
        self.setWindowTitle("Register")
        self.setGeometry(100, 100, 400, 400)

        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit(self)

        self.email_label = QLabel("Email:")
        self.email_input = QLineEdit(self)

        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)

        self.register_button = QPushButton("Register", self)
        self.register_button.clicked.connect(self.register)

        self.login_button = QPushButton("Go to Login", self)
        self.login_button.clicked.connect(self.show_login)

        layout = QVBoxLayout()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.email_label)
        layout.addWidget(self.email_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.register_button)
        layout.addWidget(self.login_button)
        layout.setAlignment(Qt.AlignCenter)
        
        self.setLayout(layout)

    def register(self):
        username = self.username_input.text()
        email = self.email_input.text()
        password = self.password_input.text()

        if not username or not email or not password:
            QMessageBox.warning(self, "Error", "All fields are required")
            return

        data = {'username': username, 'email': email, 'password': password}
        response = requests.post(f"{API_URL}/register/", json=data)

        if response.status_code == 200:
            QMessageBox.information(self, "Success", "Registration successful!")
        else:
            QMessageBox.warning(self, "Error", response.json().get("error", "Registration failed"))

    def show_login(self):
        self.stacked_widget.setCurrentIndex(0)

class WelcomeScreen(StyledWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.set_styling()

    def initUI(self):
        self.setWindowTitle("Welcome")
        self.setGeometry(100, 100, 400, 400)

        self.welcome_label = QLabel("Welcome to Jay Robotix", self)
        self.welcome_label.setFont(QFont("Arial", 18, QFont.Bold))
        self.welcome_label.setAlignment(Qt.AlignCenter)

        self.logout_button = QPushButton("Logout", self)
        self.logout_button.clicked.connect(self.logout)

        layout = QVBoxLayout()
        layout.addWidget(self.welcome_label)
        layout.addWidget(self.logout_button)
        layout.setAlignment(Qt.AlignCenter)
        
        self.setLayout(layout)

    def logout(self):
        QMessageBox.information(self, "Logged Out", "You have been logged out.")
        self.parent().setCurrentIndex(0)

class AuthApp(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Authentication System")
        self.setGeometry(100, 100, 400, 400)

        self.login_window = LoginWindow(self)
        self.register_window = RegisterWindow(self)
        self.welcome_screen = WelcomeScreen()

        self.addWidget(self.login_window)
        self.addWidget(self.register_window)
        self.addWidget(self.welcome_screen)
        self.setCurrentIndex(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    auth_app = AuthApp()
    auth_app.show()
    sys.exit(app.exec_())
