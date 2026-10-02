from PyQt6 import QtWidgets, uic
from preferences_menu import PreferencesMenu


class ApplicationsPage(QtWidgets.QWidget):
    def __init__(self, is_admin=True):
        super().__init__()

        # Load UI
        uic.loadUi("applications_page.ui", self)
        if is_admin:
            print("Admin")
        else:
            print("Normal user")

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

            if mentor_item and mentor_item.text().strip():
                self.applicationsTable.setRowHidden(row, False)
            else:
                self.applicationsTable.setRowHidden(row, True)

    def show_mentor_not_defined(self):
        for row in range(self.applicationsTable.rowCount()):
            mentor_item = self.applicationsTable.item(row, 4)

            if mentor_item and mentor_item.text().strip():
                self.applicationsTable.setRowHidden(row, True)
            else:
                self.applicationsTable.setRowHidden(row, False)

    def open_preferences(self):
        self.preferences_window = PreferencesMenu()
        self.preferences_window.show()
        self.close()


