from PyQt6 import QtWidgets, uic
from preferences_menu import PreferencesMenu


class MentorInterviewPage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Load UI
        uic.loadUi("mentor_interview_page.ui", self)

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

        self.categoryComboBox.currentTextChanged.connect(
            self.filter_by_category
        )

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
        for row in range(self.conversationsTable.rowCount()):
            self.conversationsTable.setRowHidden(row, False)

    def filter_by_category(self, category):
        for row in range(self.conversationsTable.rowCount()):
            category_item = self.conversationsTable.item(row, 3)

            if category == "All Categories":
                self.conversationsTable.setRowHidden(row, False)

            elif category_item and category_item.text().lower() == category.lower():
                self.conversationsTable.setRowHidden(row, False)

            else:
                self.conversationsTable.setRowHidden(row, True)

    def open_preferences(self):
        self.preferences_window = PreferencesMenu()
        self.preferences_window.show()
        self.close()

