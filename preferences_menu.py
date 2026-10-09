"""
Preferences Menu - Regular user menu.
Author: Waseem

Same background, header, and colors as PreferencesAdmin.
Vertical (1-column) button layout.
"""

from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFrame
)
from PyQt6.QtCore import Qt

from theme import LOGIN_QSS, center


class PreferencesMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CRM - Preferences")
        self.setMinimumSize(520, 560)
        self.resize(620, 620)

        # ✅ Force dark background — palette wins over CSS
        from theme import paint_dark_background, LOGIN_QSS
        paint_dark_background(self)
        # Same theme as login / admin
        self.setStyleSheet(LOGIN_QSS)

        self.init_ui()
        center(self)

    def init_ui(self):
        root = QVBoxLayout(self)
        root.setSpacing(14)
        root.setContentsMargins(30, 25, 30, 25)

        # ---------- Logo row ----------
        logo_row = QHBoxLayout()
        logo_row.setSpacing(12)

        self.lblAvatar = QLabel("👤")
        self.lblAvatar.setFixedSize(70, 70)
        self.lblAvatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lblAvatar.setStyleSheet(
            "font-size: 52px; color: #22d3ee; background: transparent;"
        )
        logo_row.addWidget(self.lblAvatar)

        self.lblLogoText = QLabel("WerHere")
        self.lblLogoText.setStyleSheet(
            "font-size: 30px; font-weight: 800; "
            "color: #ffffff; letter-spacing: 2px; background: transparent;"
        )
        logo_row.addWidget(self.lblLogoText)
        logo_row.addStretch()

        root.addLayout(logo_row)

        # ---------- Header bar (same as Admin) ----------
        self.frmTitle = QFrame()
        self.frmTitle.setFrameShape(QFrame.Shape.NoFrame)
        self.frmTitle.setStyleSheet(
    "QFrame#frmTitle {"
    "  background: transparent;"
    "  border: none;"
    "  border-left: 4px solid #22d3ee;"
    "  border-radius: 0px;"
    "  min-height: 40px;"
    "  max-height: 40px;"
    "}"
)

        title_lay = QHBoxLayout(self.frmTitle)
        title_lay.setContentsMargins(15, 0, 15, 0)

        self.lblTitle = QLabel("CRM — User Preference Menu")
        self.lblTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lblTitle.setStyleSheet(
            "color: #e6edf7;"
            "font-size: 14px;"
            "font-weight: 700;"
            "letter-spacing: 1px;"
            "background: transparent;"
        )
        title_lay.addWidget(self.lblTitle)
        root.addWidget(self.frmTitle)

        # ---------- Menu card ----------
        self.frmMenu = QFrame()
        self.frmMenu.setFrameShape(QFrame.Shape.NoFrame)
        self.frmMenu.setStyleSheet(
            "QFrame#frmMenu {"
            "  background: #131c2e;"
            "  border: 1px solid #26344f;"
            "  border-radius: 14px;"
            "}"
        )

        menu_lay = QVBoxLayout(self.frmMenu)
        menu_lay.setContentsMargins(40, 35, 40, 35)
        menu_lay.setSpacing(22)

        self.apps_btn       = self._make_btn("📄   Applications")
        self.mentor_btn     = self._make_btn("🎓   Mentor Interview")
        self.interviews_btn = self._make_btn("📋   Interviews")
        self.close_btn      = self._make_btn("❌   Close", danger=True)

        for b in (self.apps_btn, self.mentor_btn,
                  self.interviews_btn, self.close_btn):
            menu_lay.addWidget(b)

        root.addWidget(self.frmMenu)
        root.addStretch()

        # ---------- Signals ----------
        self.apps_btn.clicked.connect(self.open_applications)
        self.mentor_btn.clicked.connect(self.open_mentor)
        self.interviews_btn.clicked.connect(self.open_interviews)
        self.close_btn.clicked.connect(self.close)

    # --------------------------------------------------
    def _make_btn(self, text, danger=False):
        btn = QPushButton(text)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        if danger:
            btn.setStyleSheet(
                "QPushButton {"
                "  background: #1b2740; color: #f87171;"
                "  border: 1px solid rgba(248, 113, 113, 0.35);"
                "  border-radius: 10px;"
                "  padding: 12px 16px; min-height: 42px;"
                "  font-weight: 600; font-size: 13px;"
                "  text-align: center;"
                "}"
                "QPushButton:hover {"
                "  background: rgba(248, 113, 113, 0.14);"
                "  border: 1px solid #f87171;"
                "}"
                "QPushButton:pressed {"
                "  background: rgba(248, 113, 113, 0.22);"
                "}"
            )
        else:
            btn.setStyleSheet(
                "QPushButton {"
                "  background: #1b2740; color: #e6edf7;"
                "  border: 1px solid #26344f;"
                "  border-radius: 10px;"
                "  padding: 12px 16px; min-height: 42px;"
                "  font-weight: 600; font-size: 13px;"
                "  text-align: center;"
                "}"
                "QPushButton:hover {"
                "  border: 1px solid #22d3ee; color: #22d3ee;"
                "  background: #16213a;"
                "}"
                "QPushButton:pressed {"
                "  background: #26344f;"
                "}"
            )
        return btn

    # --------------------------------------------------
    def open_applications(self):
        from applications_page import ApplicationsPage
        self.next_window = ApplicationsPage(is_admin=False)
        self.next_window.show()
        self.close()

    def open_mentor(self):
        from mentor_interview_page import MentorInterviewPage
        self.next_window = MentorInterviewPage(is_admin=False)
        self.next_window.show()
        self.close()

    def open_interviews(self):
        from interviews_page import InterviewsPage
        self.next_window = InterviewsPage(is_admin=False)
        self.next_window.show()
        self.close()