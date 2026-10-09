"""
Applications Page
Layout loaded from ui/applications_page.ui, LOOK from the shared theme.py
(the light styles embedded in the .ui file are cleared at start-up).
"""

import os
import sys

from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QButtonGroup, QFrame

from services import data_service
from theme import apply_theme, center, page_header, populate, style_table

# Friendly header names (source keys are left untouched)
DISPLAY_NAMES = {
    "Timestamp": "Date",
    "Full Name": "Full name",
    "Email": "Mail",
    "Phone": "Telephone",
    "Postal Code": "Post Code",
    "Province": "State",
}


def _resource_path(relative_path):
    if getattr(sys, "frozen", False):
        base = getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, relative_path)


class ApplicationsPage(QtWidgets.QWidget):
    def __init__(self, is_admin=False):
        super().__init__()
        self.is_admin = is_admin

        # 1. Load the Qt Designer UI (layout only)
        uic.loadUi(_resource_path(os.path.join("ui", "applications_page.ui")), self)

        # 2. Find the table
        table = (self.findChild(QtWidgets.QTableWidget, "applicationsTable")
                 or self.findChild(QtWidgets.QTableWidget, "applicationsTabel"))
        if table is None:
            raise RuntimeError("The UI must contain a QTableWidget named 'applicationsTable'.")
        self.applicationsTable = table

        # 3. Remove the old Designer styles (they are light-coloured)
        self.setStyleSheet("")
        for w in self.findChildren(QtWidgets.QWidget):
            w.setStyleSheet("")
        self.mainFrame.setFrameShape(QFrame.Shape.NoFrame)   # no white panel

        # 4. Tell the theme what each widget is
        # header: same as the Interviews page
        self.titleLabel.hide()                       # old title from the .ui
        page = self.layout()
        page.setContentsMargins(30, 26, 30, 22)
        inner = self.mainFrame.layout()
        inner.setContentsMargins(0, 0, 0, 0)
        inner.setSpacing(16)
        inner.insertWidget(0, page_header(
            "📄", "Applications", "All candidate applications and quick filters",
            "ADMIN" if is_admin else "USER", is_admin))

        # filter buttons = exclusive "chips"
        self.group = QButtonGroup(self)
        for button in (
            self.allApplicationsButton, self.mentorDefinedButton,
            self.mentorNotDefinedButton, self.btn_previous_vit,
            self.btn_different_records, self.btn_filter_applications,
            self.btn_duplicates,
        ):
            button.setProperty("variant", "chip")
            button.setCheckable(True)
            self.group.addButton(button)
        self.allApplicationsButton.setChecked(True)

        self.searchButton.setProperty("variant", "primary")
        self.returnButton.setProperty("variant", "secondary")
        self.searchInput.setClearButtonEnabled(True)

        # 5. Apply the shared theme
        apply_theme(self)
        style_table(self.applicationsTable)
        self.setWindowTitle("Applications")
        center(self)

        # 6. Connect buttons
        self.searchButton.clicked.connect(self.search_applications)
        self.searchInput.returnPressed.connect(self.search_applications)
        self.allApplicationsButton.clicked.connect(self.show_all_applications)
        self.mentorDefinedButton.clicked.connect(self.show_mentor_defined)
        self.mentorNotDefinedButton.clicked.connect(self.show_mentor_not_defined)
        self.btn_previous_vit.clicked.connect(self.show_previous_vit)
        self.btn_duplicates.clicked.connect(self.show_duplicates)
        self.btn_different_records.clicked.connect(self.show_different_records)
        self.btn_filter_applications.clicked.connect(self.show_unique_applications)
        self.returnButton.clicked.connect(self.open_preferences)

        # 7. Load applications when the page opens
        self.show_all_applications()

    # --------------------------------------------------
    def display_results(self, result):
        """Display service results without changing source keys."""
        error = data_service.get_last_error()
        if error:
            QtWidgets.QMessageBox.warning(self, "Data Error", error)
            return

        headers, rows = result
        populate(self.applicationsTable, headers, rows)
        self.applicationsTable.setHorizontalHeaderLabels(
            [DISPLAY_NAMES.get(h, str(h)).upper() for h in headers])

    def search_applications(self):
        query = self.searchInput.text().strip()
        if not query:
            self.allApplicationsButton.setChecked(True)
            self.show_all_applications()
            return

        # a search result is not one of the filters -> un-highlight the chips
        self.group.setExclusive(False)
        for b in self.group.buttons():
            b.setChecked(False)
        self.group.setExclusive(True)

        self.display_results(data_service.search_applications(query))

    def show_all_applications(self):
        self.display_results(data_service.get_applications())

    def show_mentor_defined(self):
        self.display_results(data_service.get_mentor_defined())

    def show_mentor_not_defined(self):
        self.display_results(data_service.get_mentor_not_defined())

    def show_previous_vit(self):
        self.display_results(data_service.get_previous_vit())

    def show_duplicates(self):
        self.display_results(data_service.get_duplicate_applications())

    def show_different_records(self):
        self.display_results(data_service.get_different_records())

    def show_unique_applications(self):
        self.display_results(data_service.get_unique_applications())

    def open_preferences(self):
        if self.is_admin:
            from preferences_admin import PreferencesAdmin
            self.next_window = PreferencesAdmin()
        else:
            from preferences_menu import PreferencesMenu
            self.next_window = PreferencesMenu()
        self.next_window.show()
        self.close()