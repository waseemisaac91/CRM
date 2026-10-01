"""
Admin Menu
Dana

 (admin users only).
"""

from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton,
    QVBoxLayout, QTableWidget
)
from PyQt6.QtCore import Qt


class AdminMenu(QWidget):
    """Admin menu — UI only."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("CRM - Admin Menu")
        self.setGeometry(300, 150, 750, 560)
        self.init_ui()
        self.apply_style()

    # --------------------------------------------------
    # UI construction
    # --------------------------------------------------
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(25, 25, 25, 25)

        # Title
        title = QLabel("🛡️ Admin Menu")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setObjectName("title")
        layout.addWidget(title)

        # Action buttons
        self.event_btn = QPushButton("📅 Event Record")
        self.mail_btn = QPushButton("✉️ Mail")
        layout.addWidget(self.event_btn)
        layout.addWidget(self.mail_btn)

        # Table for calendar records
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(
            ["Event", "Date", "Participants", "Status"]
        )
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)

        # Return to Admin preferences
        self.return_btn = QPushButton("⬅️ Preferences — Return to Admin Screen")
        self.return_btn.setObjectName("returnBtn")
        self.return_btn.clicked.connect(self.go_back)
        layout.addWidget(self.return_btn)

        # Exit button
        self.exit_btn = QPushButton("❌ Exit")
        self.exit_btn.setObjectName("exitBtn")
        self.exit_btn.clicked.connect(self.close)
        layout.addWidget(self.exit_btn)

        self.setLayout(layout)

    # --------------------------------------------------
    # Styling (Red accent — admin view)
    # --------------------------------------------------
    def apply_style(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #2e1e1e;
                color: #ffffff;
                font-family: Arial, sans-serif;
                font-size: 13px;
            }
            QLabel#title {
                font-size: 22px;
                font-weight: bold;
                color: #F44336;
                padding-bottom: 8px;
            }
            QPushButton {
                padding: 10px;
                border-radius: 6px;
                background-color: #F44336;
                color: white;
                font-weight: bold;
                border: none;
            }
            QPushButton:hover { background-color: #D32F2F; }
            QPushButton:pressed { background-color: #B71C1C; }
            QPushButton#returnBtn { background-color: #607D8B; }
            QPushButton#returnBtn:hover { background-color: #455A64; }
            QPushButton#exitBtn { background-color: #333; }
            QPushButton#exitBtn:hover { background-color: #444; }
            QTableWidget {
                background-color: #3e2e2e;
                color: #fff;
                gridline-color: #555;
                border-radius: 6px;
            }
            QHeaderView::section {
                background-color: #F44336;
                color: white;
                padding: 8px;
                border: none;
            }
        """)

    # --------------------------------------------------
    # Navigation
    # --------------------------------------------------
    def go_back(self):
        """Return to the Admin Preferences screen."""
        from preferences_admin import PreferencesAdmin
        self.window = PreferencesAdmin()
        self.window.show()
        self.close()