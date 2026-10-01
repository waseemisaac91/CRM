"""
Login Window - Starting point of the app.
Author: Waseem
"""

from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QMessageBox
)
from PyQt6.QtCore import Qt
from preferences_menu import PreferencesMenu
from preferences_admin import PreferencesAdmin


class LoginWindow(QWidget):
    """Custom login page."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("CRM - Login")
        self.setGeometry(400, 200, 420, 360)
        self.init_ui()
        self.apply_style()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(40, 40, 40, 40)

        # Title
        title = QLabel("🔐 CRM Login")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setObjectName("title")
        layout.addWidget(title)

        # Username
        layout.addWidget(QLabel("Username:"))
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        layout.addWidget(self.username_input)

        # Password
        layout.addWidget(QLabel("Password:"))
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)

        # Warning label (empty for now)
        self.warning_label = QLabel("")
        self.warning_label.setObjectName("warning")
        self.warning_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.warning_label)

        # Login button
        self.login_btn = QPushButton("Login")
        self.login_btn.clicked.connect(self.handle_login)
        layout.addWidget(self.login_btn)

        # Close button
        self.close_btn = QPushButton("Close")
        self.close_btn.setObjectName("closeBtn")
        self.close_btn.clicked.connect(self.close)
        layout.addWidget(self.close_btn)

        self.setLayout(layout)

    def apply_style(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e2e;
                color: #ffffff;
                font-family: Arial, sans-serif;
                font-size: 14px;
            }
            QLabel#title {
                font-size: 22px;
                font-weight: bold;
                color: #4CAF50;
                padding-bottom: 10px;
            }
            QLabel#warning {
                color: #f44336;
                font-weight: bold;
            }
            QLineEdit {
                padding: 10px;
                border-radius: 8px;
                background-color: #2e2e3e;
                border: 1px solid #444;
                color: #fff;
            }
            QLineEdit:focus {
                border: 1px solid #4CAF50;
            }
            QPushButton {
                padding: 12px;
                border-radius: 8px;
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
                border: none;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
            QPushButton#closeBtn {
                background-color: #555;
            }
            QPushButton#closeBtn:hover {
                background-color: #666;
            }
        """)

    def handle_login(self):
        """Navigate to Preferences. Login check comes later."""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        # Placeholder logic — no real auth yet
        if not username or not password:
            self.warning_label.setText("⚠️ Please enter username and password.")
            return

        # Decide which preferences window to open (hardcoded for now)
        # For testing: any user with "admin" in the name → admin menu
        if "admin" in username.lower():
            self.prefs = PreferencesAdmin()
        else:
            self.prefs = PreferencesMenu()

        self.prefs.show()
        self.close()