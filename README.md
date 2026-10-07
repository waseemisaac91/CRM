# CRM Capstone Project

A desktop CRM built with **Python, PyQt6 and Qt Designer** to manage candidates who apply to
the VIT program (IT training for refugees). Instead of opening several Google Drive files, the
app reads the data from Google Drive and Google Calendar and shows it in searchable, filterable tables.

## Features

| Window | What it does |
|---|---|
| **Login** | Checks username / password against the *Users* file in Drive. `Admin` -> Preferences Admin, `User` -> Preferences. Shows success / warning text. |
| **Preferences / Preferences Admin** | Navigation to Applications, Mentor Interview, Interviews (and Admin Menu for admins). |
| **Applications** | Search (name starts with...), all applications, mentor meeting identified / not identified, duplicate records, previous VIT check, different record, application filter (unique), return. |
| **Mentor Interview** | Search, all conversations, filter by recommendation (combo box), return. |
| **Interviews** | Search, projects sent, projects received, return. |
| **Admin Menu** | Loads events from Google Calendar into a table and e-mails the participants of the selected event. |

## Project structure

```
crm/
|-- main.py                      entry point
|-- login_window.py, login.py    login window (+ Qt Designer generated UI)
|-- preferences_menu.py          user menu
|-- preferences_admin.py, admin_preferences.py   admin menu (+ generated UI)
|-- applications_page.py         Applications window
|-- mentor_interview_page.py     Mentor window
|-- interviews_page.py           Interviews window
|-- admin_menu.py                Admin window (calendar + e-mail)
|-- google_service.py            Drive connection + login check
|-- services/
|   |-- google_drive_service.py  spreadsheet IDs + gspread client
|   |-- sheets_service.py        reads sheets, auto-detects header and columns
|   |-- data_service.py          search / filter logic for the pages
|   |-- google_calendar_service.py   Calendar events
|   `-- email_service.py         sends e-mails
|-- check_drive.py, debug_calendar.py   connection tests
|-- docs/GOOGLE_CONNECTION_GUIDE.md     Drive / Calendar / E-mail setup
|-- credentials/                 service_account.json (NOT in GitHub)
|-- .env                         e-mail login (NOT in GitHub)
`-- requirements.txt
```

## Installation

```
git clone <your-repo-url>
cd crm
python -m venv .venv
.venv\Scripts\activate          # Windows   (Linux/Mac: source .venv/bin/activate)
pip install -r requirements.txt
```

Then follow **[docs/GOOGLE_CONNECTION_GUIDE.md](docs/GOOGLE_CONNECTION_GUIDE.md)** to add
`credentials/service_account.json` and `.env`, and run:

```
python check_drive.py     # verify Drive
python debug_calendar.py  # verify Calendar
python main.py            # start the app
```

## Build the .exe

```
pip install pyinstaller
pyinstaller --noconfirm --onefile --windowed --name CRM main.py
```
Place `credentials/` and `.env` next to `dist/CRM.exe`.

## Usage scenarios

1. **User searches a candidate:** Login (User) -> Preferences -> Applications -> type `As` -> Search ->
   all names with a word starting with "as" are shown -> Return.
2. **Admin checks repeated candidates:** Login (Admin) -> Applications -> Duplicate Records / Previous VIT Check.
3. **Admin informs participants:** Login (Admin) -> Admin Menu -> Refresh Events -> select an event ->
   Send Emails to Participants.

## How the data rules work

- **Search:** matches the start of any word in the name or surname (`As` -> *Asma Ali*, *Omar Asaad*).
- **Duplicate records:** same name **and** e-mail more than once - only those people are shown.
- **Application filter:** the same key, each person shown once.
- **Previous VIT check:** applicants whose name also exists in VIT1 and/or VIT2 (a "Found In" column is added).
- **Different record:** people who are in only one of VIT1 / VIT2.
- **Mentor meeting identified:** the *Mentor meeting* column is not empty and not "No".

## Team

- Waseem - login, preferences, admin menu (Drive +Calendar + e-mail)
- Dana - mentor and interviews pages
- Mohammed  Application Pages
- (add the remaining members and the Trello / UML links here)

## Security

Never commit `credentials/`, `.env`, `client_secret*.json` or `token.json` (they are in `.gitignore`).
