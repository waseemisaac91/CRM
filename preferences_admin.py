"""
Preferences Admin Menu
Author: Waseem

Matches the login theme (dark navy + cyan).
Header is a flat bar with a left cyan accent stripe.
"""

from PyQt6.QtWidgets import QWidget, QApplication, QFrame
from PyQt6.QtCore import Qt

from admin_preferences import Ui_AdminPreferences
from theme import LOGIN_QSS, center


class PreferencesAdmin(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_AdminPreferences()
        self.ui.setupUi(self)

        # Clear any leftover styles from the .ui
        for w in self.findChildren(QWidget):
            w.setStyleSheet("")
         # ✅ Force dark background — palette wins over CSS
        from theme import paint_dark_background
        paint_dark_background(self)
        # Apply the shared login theme (background now applies
        # because AdminPreferences is listed in LOGIN_QSS)
        self.setStyleSheet(LOGIN_QSS)

        # ---------- Logo ----------
        self.ui.lblAvatar.setStyleSheet(
            "font-size: 52px; color: #22d3ee; background: transparent;"
        )
        self.ui.lblLogoText.setText("WerHere")
        self.ui.lblLogoText.setStyleSheet(
            "font-size: 30px; font-weight: 800; "
            "color: #ffffff; letter-spacing: 2px; background: transparent;"
        )

        # ---------- Header bar — flat, with left accent stripe ----------
        self.ui.frmTitle.setFrameShape(QFrame.Shape.NoFrame)
        self.ui.frmTitle.setStyleSheet("""
            QFrame#frmTitle {
                background: #131c2e;
                border: 1px solid #26344f;
                border-left: 4px solid #22d3ee;
                border-radius: 10px;
                min-height: 40px;
                max-height: 40px;
            }
        """)
        self.ui.lblTitle.setStyleSheet(
            "color: #e6edf7;"
            "font-size: 14px;"
            "font-weight: 700;"
            "letter-spacing: 1px;"
            "background: transparent;"
        )

        # ---------- Menu card ----------
        self.ui.frmMenu.setFrameShape(QFrame.Shape.NoFrame)
        self.ui.frmMenu.setStyleSheet("""
            QFrame#frmMenu {
                background: #131c2e;
                border: 1px solid #26344f;
                border-radius: 14px;
            }
        """)

        # ---------- Standard buttons ----------
        standard_qss = """
            QPushButton {
                background: #1b2740;
                color: #e6edf7;
                border: 1px solid #26344f;
                border-radius: 10px;
                padding: 12px 16px;
                min-height: 42px;
                font-weight: 600;
                font-size: 13px;
                text-align: center;
            }
            QPushButton:hover {
                border: 1px solid #22d3ee;
                color: #22d3ee;
                background: #16213a;
            }
            QPushButton:pressed {
                background: #26344f;
            }
        """
        for btn in (self.ui.btnApplications,
                    self.ui.btnMentorInterview,
                    self.ui.btnInterviews,
                    self.ui.btnMainMenu):
            btn.setStyleSheet(standard_qss)

        # ---------- Admin button (amber) ----------
        self.ui.btnAdmin.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #fbbf24, stop:1 #f59e0b);
                color: #04222b;
                border: none;
                border-radius: 10px;
                padding: 12px 16px;
                min-height: 42px;
                font-weight: 700;
                font-size: 13px;
                text-align: center;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #fcd34d, stop:1 #fbbf24);
            }
            QPushButton:pressed {
                background: #d97706;
            }
        """)

        # ---------- Exit button (red danger) ----------
        self.ui.btnExit.setStyleSheet("""
            QPushButton {
                background: #1b2740;
                color: #f87171;
                border: 1px solid rgba(248, 113, 113, 0.35);
                border-radius: 10px;
                padding: 12px 16px;
                min-height: 42px;
                font-weight: 600;
                font-size: 13px;
                text-align: center;
            }
            QPushButton:hover {
                background: rgba(248, 113, 113, 0.14);
                border: 1px solid #f87171;
            }
            QPushButton:pressed {
                background: rgba(248, 113, 113, 0.22);
            }
        """)

        self.setWindowTitle("CRM - Admin Preferences")
        center(self)

        # ---------- Signals ----------
        self.ui.btnApplications.clicked.connect(self.open_applications)
        self.ui.btnMentorInterview.clicked.connect(self.open_mentor)
        self.ui.btnInterviews.clicked.connect(self.open_interviews)
        self.ui.btnAdmin.clicked.connect(self.open_admin_menu)
        self.ui.btnMainMenu.clicked.connect(self.back_to_login)
        self.ui.btnExit.clicked.connect(self.close)

    # --------------------------------------------------
    def open_applications(self):
        from applications_page import ApplicationsPage
        self.next_window = ApplicationsPage(is_admin=True)
        self.next_window.show()
        self.close()

    def open_mentor(self):
        from mentor_interview_page import MentorInterviewPage
        self.next_window = MentorInterviewPage(is_admin=True)
        self.next_window.show()
        self.close()

    def open_interviews(self):
        from interviews_page import InterviewsPage
        self.next_window = InterviewsPage(is_admin=True)
        self.next_window.show()
        self.close()

    def open_admin_menu(self):
        from admin_menu import AdminMenu
        self.next_window = AdminMenu()
        self.next_window.show()
        self.close()

    def back_to_login(self):
        from login_window import LoginWindow
        self.next_window = LoginWindow()
        self.next_window.show()
        self.close()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    w = PreferencesAdmin()
    w.show()
    sys.exit(app.exec())