import os
from PyQt6 import QtWidgets, uic

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class MentorInterviewPage(QtWidgets.QWidget):
    def __init__(self, is_admin=False):
        super().__init__()
        self.is_admin = is_admin  # to know where to return

        # Load UI (path relative to this file, not the working directory)
        uic.loadUi(os.path.join(BASE_DIR, "mentor_interview_page.ui"), self)

        # Categories
        self.categoryComboBox.addItems([
            "All Categories",
            "Accepted",
            "Rejected",
            "Pending"
        ])

        # Connect buttons
        self.searchButton.clicked.connect(self.search_conversations)
        self.allConversations.clicked.connect(self.show_all_conversations)
        self.categoryComboBox.currentTextChanged.connect(self.filter_by_category)
        self.returnButton.clicked.connect(self.open_preferences)

    def search_conversations(self):
        search_text = self.searchInput.text().lower()

        for row in range(self.conversationsTable.rowCount()):
            match = False

            for column in range(self.conversationsTable.columnCount()):
                item = self.conversationsTable.item(row, column)

                if item and search_text in item.text().lower():
                    match = True
                    break

            self.conversationsTable.setRowHidden(row, not match)

    def show_all_conversations(self):
        self.categoryComboBox.setCurrentIndex(0)  # keep combo in sync
        for row in range(self.conversationsTable.rowCount()):
            self.conversationsTable.setRowHidden(row, False)

    def filter_by_category(self, category):
        for row in range(self.conversationsTable.rowCount()):
            category_item = self.conversationsTable.item(row, 3)

            if category == "All Categories":
                hidden = False
            else:
                hidden = not (category_item and
                              category_item.text().strip().lower() == category.lower())
            self.conversationsTable.setRowHidden(row, hidden)

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