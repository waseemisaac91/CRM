import os

from PyQt6 import QtWidgets, uic
from services import data_service


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class ApplicationsPage(QtWidgets.QWidget):
    def __init__(self, is_admin=False):
        super().__init__()
        self.is_admin = is_admin

        # Find the UI file
        ui_path = os.path.join(BASE_DIR, "applications_page.ui")

        if not os.path.isfile(ui_path):
            ui_path = os.path.join(
                BASE_DIR, "ui", "applications_page.ui"
            )

        ui_path = os.path.join(
            BASE_DIR, "ui", "applications_page.ui"
        )

        ui_path = os.path.join(BASE_DIR, "ui", "applications_page.ui")
        uic.loadUi(ui_path, self)
        
        # Support the table name in uploaded design
        table = self.findChild(
            QtWidgets.QTableWidget, "applicationsTable"
        )

        if table is None:
            table = self.findChild(
                QtWidgets.QTableWidget, "applicationsTabel"
            )

        if table is None:
            raise RuntimeError(
                "The Applications table was not found in the UI."
            )

        self.applicationsTable = table

        # Display only: editing cells does not save to Google Sheets
        self.applicationsTable.setEditTriggers(
            QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers
        )
        self.applicationsTable.setAlternatingRowColors(True)
        self.applicationsTable.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows
        )

        # Existing buttons
        self.searchButton.clicked.connect(
            self.search_applications
        )
        self.allApplicationsButton.clicked.connect(
            self.show_all_applications
        )
        self.mentorDefinedButton.clicked.connect(
            self.show_mentor_defined
        )
        self.mentorNotDefinedButton.clicked.connect(
            self.show_mentor_not_defined
        )
        self.returnButton.clicked.connect(
            self.open_preferences
        )

        self.btn_previous_vit.clicked.connect(
            self.show_previous_vit
        )
        self.btn_duplicates.clicked.connect(
            self.show_duplicates
        )
        self.btn_different_records.clicked.connect(
            self.show_different_records
        )
        self.btn_filter_applications.clicked.connect(
            self.filter_applications
        )

        # Search by pressing Enter
        self.searchInput.returnPressed.connect(
            self.search_applications
        )

        # Load applications when opening the page
        self.show_all_applications()

    def display_results(self, result):
        """Fill the table with data returned by data_service."""
        error = data_service.get_last_error()

        if error:
            QtWidgets.QMessageBox.warning(
                self,
                "Data Error",
                error
            )
            return

        headers, rows = result
        table = self.applicationsTable

        sorting_enabled = table.isSortingEnabled()
        table.setSortingEnabled(False)

        try:
            table.clearContents()
            table.setRowCount(0)

            # Use the headers returned by Google Sheets
            table.setColumnCount(len(headers))
            table.setHorizontalHeaderLabels(headers)
            table.setRowCount(len(rows))

            for row_index, record in enumerate(rows):
                table.setRowHidden(row_index, False)

                for column_index, header in enumerate(headers):
                    value = record.get(header, "")
                    text = "" if value is None else str(value)

                    item = QtWidgets.QTableWidgetItem(text)
                    table.setItem(
                        row_index,
                        column_index,
                        item
                    )

            table.resizeColumnsToContents()

        finally:
            table.setSortingEnabled(sorting_enabled)

    def show_all_applications(self):
        result = data_service.get_applications()
        self.display_results(result)

    def search_applications(self):
        query = self.searchInput.text().strip()

        if not query:
            self.show_all_applications()
            return

        result = data_service.search_applications(query)
        self.display_results(result)

    def show_mentor_defined(self):
        result = data_service.get_mentor_defined()
        self.display_results(result)

    def show_mentor_not_defined(self):
        result = data_service.get_mentor_not_defined()
        self.display_results(result)

    def show_duplicates(self):
        result = data_service.get_duplicate_applications()
        self.display_results(result)

    def filter_applications(self):
        result = data_service.get_unique_applications()
        self.display_results(result)

    def show_previous_vit(self):
        result = data_service.get_previous_vit()
        self.display_results(result)

    def show_different_records(self):
        result = data_service.get_different_records()
        self.display_results(result)

    def open_preferences(self):
        """Return to the menu matching the user's role."""
        if self.is_admin:
            from preferences_admin import PreferencesAdmin
            self.next_window = PreferencesAdmin()
        else:
            from preferences_menu import PreferencesMenu
            self.next_window = PreferencesMenu()

        self.next_window.show()
        self.close()
