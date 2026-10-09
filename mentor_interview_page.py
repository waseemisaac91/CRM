"""
Mentor Interview Page
Author: Dana
Layout loaded from ui/mentor_interview_page.ui.
Header + theme come from the shared theme.py (same as Interviews page).
Search filters the loaded rows instantly (names STARTING with typed letters).
"""

import os
import sys

from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget

from services.data_service import (
    get_all_conversations, get_conversations_by_recommendation,
    get_last_error, name_matches,
)
from theme import (
    apply_theme, center, page_header, populate, set_status, style_table,
)


def _resource_path(relative_path):
    if getattr(sys, "frozen", False):
        base = getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, relative_path)


COLS = [
    "Date", "VIT Group", "Candidate Name", "Mentor Name",
    "Score", "Recommendation", "Secondary Score", "Notes",
]
NAME_COL = "Candidate Name"
ALL_RECS = "All Recommendations"


class MentorInterviewPage(QWidget):
    def __init__(self, is_admin=False):
        super().__init__()
        self.is_admin = is_admin
        self.rows = []

        # ---------- Load .ui (layout only) ----------
        uic.loadUi(
            _resource_path(os.path.join("ui", "mentor_interview_page.ui")),
            self,
        )

        # ---------- Aliases ----------
        self.search_input = self.searchInput
        self.all_btn      = self.allConversationsButton
        self.combo        = self.categoryComboBox
        self.table        = self.conversationsTable
        self.status       = self.statusLabel
        self.return_btn   = self.returnButton

        # ---------- Tell the theme what each widget is ----------
        self.cardFrame.setObjectName("card")
        self.status.setObjectName("status")
        self.all_btn.setProperty("variant", "chip")
        self.all_btn.setCheckable(True)
        self.all_btn.setChecked(True)
        self.return_btn.setProperty("variant", "secondary")

        # ---------- Header: same as the Interviews page ----------
        root = self.layout()
        root.setContentsMargins(30, 26, 30, 22)
        root.setSpacing(16)
        root.insertWidget(0, page_header(
            "🎓",
            "Mentor Interview",
            "Conversations and recommendations from mentors",
            "ADMIN" if is_admin else "USER",
            is_admin,
        ))

        # ---------- Apply the shared theme ----------
        apply_theme(self)
        style_table(self.table)
        self.setWindowTitle("CRM - Mentor Interview")
        center(self)

        # ---------- Signals ----------
        self.search_input.textChanged.connect(self.render)   # live search
        self.all_btn.clicked.connect(self.on_all)
        self.combo.currentTextChanged.connect(self.on_combo_changed)
        self.return_btn.clicked.connect(self.go_back)

        # ---------- Initial load ----------
        self.load(get_all_conversations)

    # --------------------------------------------------
    def load(self, func):
        self.search_input.blockSignals(True)
        self.search_input.clear()
        self.search_input.blockSignals(False)

        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        try:
            headers, rows = func()
            self.rows = rows
        finally:
            QApplication.restoreOverrideCursor()

        self.render()

    def render(self):
        q = self.search_input.text().strip()

        rows = self.rows
        if isinstance(rows, tuple):
            rows = rows[1]
        total = len(rows)

        if q:
            rows = [r for r in rows if name_matches(q, r.get(NAME_COL, ""))]

        populate(self.table, COLS, rows)

        err = get_last_error()
        if err:
            set_status(self.status, f"⚠  {err}", True)
        elif q:
            set_status(self.status, f"{len(rows)} of {total} record(s) match “{q}”")
        else:
            set_status(self.status, f"{len(rows)} record(s)")

    # --------------------------------------------------
    def on_all(self):
        self.all_btn.setChecked(True)
        self.combo.blockSignals(True)
        self.combo.setCurrentIndex(0)
        self.combo.blockSignals(False)
        self.load(lambda: get_all_conversations(refresh=True))

    def on_combo_changed(self, value):
        self.all_btn.setChecked(value == ALL_RECS)
        if value == ALL_RECS:
            self.load(get_all_conversations)
        else:
            self.load(lambda: get_conversations_by_recommendation(value))

    # --------------------------------------------------
    def go_back(self):
        if self.is_admin:
            from preferences_admin import PreferencesAdmin
            self.next_window = PreferencesAdmin()
        else:
            from preferences_menu import PreferencesMenu
            self.next_window = PreferencesMenu()
        self.next_window.show()
        self.close()