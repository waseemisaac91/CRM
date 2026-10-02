import os
from PyQt6 import QtWidgets, uic

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class ApplicationsPage(QtWidgets.QWidget):
    def __init__(self, is_admin=False):
        super().__init__()
        self.is_admin = is_admin  # to know where to return

        # Load UI (path relative to this file, not the working directory)
        uic.loadUi(os.path.join(BASE_DIR, "applications_page.ui"), self)

        # Connect buttons
        self.searchButton.clicked.connect(self.search_applications)
        self.allApplicationsButton.clicked.connect(self.show_all_applications)
        self.mentorDefinedButton.clicked.connect(self.show_mentor_defined)
        self.mentorNotDefinedButton.clicked.connect(self.show_mentor_not_defined)
        self.returnButton.clicked.connect(self.open_preferences)

    def search_applications(self):
        search_text = self.searchInput.text().lower()

        for row in range(self.applicationsTable.rowCount()):
            match = False

            for column in range(self.applicationsTable.columnCount()):
                item = self.applicationsTable.item(row, column)

                if item and search_text in item.text().lower():
                    match = True
                    break

            self.applicationsTable.setRowHidden(row, not match)

    def show_all_applications(self):
        for row in range(self.applicationsTable.rowCount()):
            self.applicationsTable.setRowHidden(row, False)

    def show_mentor_defined(self):
        for row in range(self.applicationsTable.rowCount()):
            mentor_item = self.applicationsTable.item(row, 4)
            defined = bool(mentor_item and mentor_item.text().strip())
            self.applicationsTable.setRowHidden(row, not defined)

    def show_mentor_not_defined(self):
        for row in range(self.applicationsTable.rowCount()):
            mentor_item = self.applicationsTable.item(row, 4)
            defined = bool(mentor_item and mentor_item.text().strip())
            self.applicationsTable.setRowHidden(row, defined)

    def open_preferences(self):
        """Return to the correct Preferences screen (admin or regular)."""
        if self.is_admin:
            from preferences_admin import PreferencesAdmin
            self.next_window = PreferencesAdmin()
        else:
            from preferences_menu import PreferencesMenu
            self.next_window = PreferencesMenu()
        self.next_window.show()
        self.close()