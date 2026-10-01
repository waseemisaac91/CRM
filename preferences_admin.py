"""
Preferences Admin Menu - Admin user menu.
waseem 

This window opens after login when the user is an admin.
It contains:
    - Applications button      → Applications Page
    - Mentor Interview button  → Mentor Interview Page
    - Interviews button        → Interviews Page
    - Admin button             → Admin Menu
    - Close button             → Exit application
"""

from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout
)
from PyQt6.QtCore import Qt


class PreferencesAdmin(QWidget):
    """Menu for admin users."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("CRM - Preferences (Admin)")
        self.setGeometry(400, 200, 450, 480)
        self.init_ui()
        self.apply_style()

    # --------------------------------------------------
    # UI construction
    # --------------------------------------------------
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(40, 40, 40, 40)

        # Title with admin badge
        title = QLabel("⚙️ Preferences — Admin 🛡️")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setObjectName("title")
        layout.addWidget(title)

        # Subtitle to distinguish from normal Preferences
        subtitle = QLabel("You are logged in as an administrator")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setObjectName("subtitle")
        layout.addWidget(subtitle)

        layout.addSpacing(10)

        # Navigation buttons (same 3 as regular Preferences)
        self.apps_btn = QPushButton("📄  Applications")
        self.apps_btn.clicked.connect(self.open_applications)

        self.mentor_btn = QPushButton("🎓  Mentor Interview")
        self.mentor_btn.clicked.connect(self.open_mentor)

        self.interviews_btn = QPushButton("📋  Interviews")
        self.interviews_btn.clicked.connect(self.open_interviews)

        # Admin-specific button
        self.admin_btn = QPushButton("🛡️  Admin Menu")
        self.admin_btn.setObjectName("adminBtn")
        self.admin_btn.clicked.connect(self.open_admin)

        layout.addWidget(self.apps_btn)
        layout.addWidget(self.mentor_btn)
        layout.addWidget(self.interviews_btn)
        layout.addWidget(self.admin_btn)

        layout.addSpacing(10)

        # Close button
        self.close_btn = QPushButton("❌  Close")
        self.close_btn.setObjectName("closeBtn")
        self.close_btn.clicked.connect(self.close)
        layout.addWidget(self.close_btn)

        self.setLayout(layout)

    # --------------------------------------------------
    # Styling (Orange accent = admin view)
    # --------------------------------------------------
    def apply_style(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #2a2a3e;
                color: #ffffff;
                font-family: Arial, sans-serif;
                font-size: 14px;
            }
            QLabel#title {
                font-size: 22px;
                font-weight: bold;
                color: #FF9800;
                padding-bottom: 4px;
            }
            QLabel#subtitle {
                font-size: 12px;
                color: #b0b0c0;
                font-style: italic;
                padding-bottom: 6px;
            }
            QPushButton {
                padding: 12px;
                border-radius: 8px;
                background-color: #2196F3;
                color: white;
                font-weight: bold;
                border: none;
                text-align: left;
            }
            QPushButton:hover  { background-color: #1976D2; }
            QPushButton:pressed { background-color: #1565C0; }

            /* Admin button — distinct orange */
            QPushButton#adminBtn {
                background-color: #FF9800;
            }
            QPushButton#adminBtn:hover  { background-color: #F57C00; }
            QPushButton#adminBtn:pressed { background-color: #EF6C00; }

            /* Close button — grey */
            QPushButton#closeBtn {
                background-color: #555;
            }
            QPushButton#closeBtn:hover { background-color: #666; }
        """)

    # --------------------------------------------------
    # Navigation handlers
    # --------------------------------------------------
    def open_applications(self):
        from applications_page import ApplicationsPage
        self.window = ApplicationsPage(is_admin=True)
        self.window.show()
        self.close()

    def open_mentor(self):
        from mentor_interview_page import MentorInterviewPage
        self.window = MentorInterviewPage()
        self.window.show()
        self.close()

    def open_interviews(self):
        from interviews_page import InterviewsPage
        self.window = InterviewsPage()
        self.window.show()
        self.close()

    def open_admin(self):
        from admin_menu import AdminMenu
        self.window = AdminMenu()
        self.window.show()
        self.close()
