"""
Interviews Page
 Dana

"""

from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout
)
from PyQt6.QtCore import Qt


class InterviewsPage(QWidget):
    """Interviews page — UI only."""

    def __init__(self, is_admin=False):
        super().__init__()
        self.is_admin = is_admin  # to know where to return
        self.setWindowTitle("CRM - Interviews")
        self.setGeometry(350, 200, 550, 430)
        self.init_ui()
        self.apply_style()

    # --------------------------------------------------
    # UI construction
    # --------------------------------------------------
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)

        # Title
        title = QLabel("📋 Interviews")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setObjectName("title")
        layout.addWidget(title)

        # Search row
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search interviews...")
        self.search_btn = QPushButton("🔍 Search")
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_btn)
        layout.addLayout(search_layout)

        # Action buttons
        self.sent_btn = QPushButton("📤 Project Sent")
        self.received_btn = QPushButton("📥 Project Received")
        layout.addWidget(self.sent_btn)
        layout.addWidget(self.received_btn)

        # Return button
        self.return_btn = QPushButton("⬅️ Return to Preferences Screen")
        self.return_btn.setObjectName("returnBtn")
        self.return_btn.clicked.connect(self.go_back)
        layout.addWidget(self.return_btn)

        self.setLayout(layout)

    # --------------------------------------------------
    # Styling (Pink accent to differentiate)
    # --------------------------------------------------
    def apply_style(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #2e1e2e;
                color: #ffffff;
                font-family: Arial, sans-serif;
                font-size: 14px;
            }
            QLabel#title {
                font-size: 22px;
                font-weight: bold;
                color: #E91E63;
                padding-bottom: 8px;
            }
            QLineEdit {
                padding: 8px;
                border-radius: 6px;
                background-color: #3e2e3e;
                border: 1px solid #555;
                color: #fff;
            }
            QLineEdit:focus {
                border: 1px solid #E91E63;
            }
            QPushButton {
                padding: 10px;
                border-radius: 6px;
                background-color: #E91E63;
                color: white;
                font-weight: bold;
                border: none;
            }
            QPushButton:hover { background-color: #C2185B; }
            QPushButton:pressed { background-color: #AD1457; }
            QPushButton#returnBtn { background-color: #607D8B; }
            QPushButton#returnBtn:hover { background-color: #455A64; }
        """)

    # --------------------------------------------------
    # Navigation
    # --------------------------------------------------
    def go_back(self):
        """Return to the correct Preferences screen."""
        if self.is_admin:
            from preferences_admin import PreferencesAdmin
            self.next_window = PreferencesAdmin()
        else:
            from preferences_menu import PreferencesMenu
            self.next_window = PreferencesMenu()
        self.next_window.show()
        self.close()