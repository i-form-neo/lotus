# 🪷 **Lotus** - Your Personal Assistant Bot 🪷

Lotus is a console application designed to help you manage your contacts and notes efficiently. Keep track of important information like phone numbers, addresses, emails, and birthdays for your contacts, and organize your thoughts with notes that include titles, creation/update dates, and tags.

---

## ✨ Features
### Contacts Management:

* Add Contacts: Store names, phone numbers, birthdays, emails, and addresses.

* Update Information: Easily modify existing phone numbers or add new ones, birthdays, emails, and addresses.

* Remove Contacts: Delete contacts when they are no longer needed.

* View All Contacts: Display all your contacts in a clear, sortable table.

* Search Contacts: Find contacts by name, phone number, or email.

* Birthday Reminders: Get a list of upcoming birthdays within a specified number of days.

### Notes Management:

* Create Notes: Add new notes with a title and text content.

* View All Notes: See all your notes in a sortable table, including creation and modification dates.

* Update Information: updating, deleting, and tagging notes

* Search Notes: Find notes by tags or title

---

## 🚀 Getting Started

### Prerequisites

Python 3.10 or higher

### Installation
`pip install git+https://github.com/i-form-neo/lotus.git`

---

### Usage

To start the Lotus bot, run following command:

`python -m lotus_bot.main`

You'll see a welcome message and a prompt Enter a command:.

* Type your command and press Enter.

* Use Tab for auto-completion of commands.

* Enclose multi-word arguments in quotes, e.g., "John Doe" or "Kyiv, Ukraine".

---

### 📝 Commands

Lotus provides a user-friendly command-line interface. Here's a list of available commands and their usage:

| Command                        | Usage                                         | Description                                                  |
| :----------------------------- | :---------------------------------------------| :------------------------------------------------------------|
| hello                          | hello                                         | Greets the bot.                                              |
| add-phone name phone           | add-phone "John Doe" +380123456789            | Adds a new contact or a phone to an existing contact.        |
| add-birthday name DD.MM.YYYY   | add-birthday "John Doe" 22.07.2000            | Adds or updates a birthday for a contact.                    |
| add-email	name email           | add-email "John Doe" john.doe@example.com     | Adds or updates an email for a contact.                      |
| add-address name address       | add-address "John Doe" "Kyiv, Ukraine"        | Adds or updates an address for a contact.                    |
| change name old_phone new_phone| change "John Doe" +380123456789 +380987654321 | Changes an existing phone number for a contact.              |
| remove name                    | remove "John Doe"                             | Removes a contact by name.                                   |
| all [sort-by-column] [desc/reverse/true]| all birthday desc                    | Displays all contacts, optionally sorted.                    |
| phone name                     | phone "John Doe"                              | Shows phone numbers for a specific contact.                  |
| show-birthday	name             | show-birthday "John Doe"                      | Shows the birthday for a specific contact.                   |
| birthdays	num-of-days          | birthdays 10                                  | Lists upcoming birthdays within the next N days.             |
| find-by-phone	phone            | find-by-phone +380123456789                   | Finds and displays a contact by phone number.                |
| find-by-email email	         | find-by-email john.doe@example.com            | Finds and displays a contact by email.                       |
| add-note title text [comma-separated-tags]| add-note "Meeting Notes" "Discuss project proposal" tag1,meeting| Adds a new note with a title, text and optionally tags.|
| add-tag id tag                 | add-tag 1 important                           | Adds a tag to an existing note.                              |
| find-by-tag tag                | find-by-tag important                         | Fiind all notes with the tag.                                |
| find-by-title title            | find-by-tag important                         | Fiind all notes with the tag.                                |
| edit-note id new-text          | edit-note 1 "Update project proposal"         | Updates a note with a new text.                              |
| all-notes [sort-by-column] [desc/reverse/true] | all-notes title desc.         | Displays all notes, optionally sorted.                       |
| help                           | help                                          | Displays this help message.                                  |
| exit / quit / close            | exit                                          | Exits the application.                                       |

---
