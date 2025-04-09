import gspread
from google.oauth2.service_account import Credentials

# constant variable
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('friend-finder')

#function to add a new contact.
def add_contact():
    print("\n--- Add New Contact ---")
    try:
        name = input("Name: ").strip()
        phone = input("Phone: ").strip()
        email = input("Email: ").strip()
        notes = input("Notes (optional): ").strip()

        if not name or not phone or not email:
            print("⚠️ Name, phone, and email are required.")
            return

        worksheet = SHEET.sheet1
        worksheet.append_row([name, phone, email, notes])
        print("✅ Contact added successfully!")

    except Exception as e:
        print("❌ An error occurred while adding the contact.")
        print(f"Error details: {e}")

#function to view all contacts.
def view_contacts():
    print("\n--- All Contacts ---")
    print()
    try:
        worksheet = SHEET.sheet1
        contacts = worksheet.get_all_values()

        if len(contacts) <= 1:
            print("📭 No contacts found.")
            return

        for i, contact in enumerate(contacts, start=1):
            print(f"{i}. {contact[0]} | {contact[1]} | {contact[2]} | {contact[3]}")

    except Exception as e:
        print("❌ Failed to retrieve contacts.")
        print(f"Error: {e}")

# fucntion to search contact by name.
def search_contact():
    print("\n--- Search Contact by Name ---")
    try:
        name_to_search = input("Enter name to search: ").strip().lower()
        worksheet = SHEET.sheet1
        contacts = worksheet.get_all_values()

        # Check if there is any contacts already.
        if len(contacts) <= 1:
            print("📭 No contacts found.")
            return

        found = False
        
        # Iterate through the contacts to find the matching name.
        for contact in contacts[1:]:
            name = contact[0].strip().lower()
            if name == name_to_search:
                print(f"🔎 Found: {contact[0]} | {contact[1]} | {contact[2]} | {contact[3]}")
                found = True
                break

        # If no contact is found, print a message.
        if not found:
            print("❌ Contact not found.")

    except Exception as e:
        print("❌ Failed to search contacts.")
        print(f"Error: {e}")


def edit_contact():
    print("\n--- Edit Contact ---")
    try:
        name_to_edit = input("Enter name of the contact to edit: ").strip().lower()
        worksheet = SHEET.sheet1
        contacts = worksheet.get_all_values()

        if len(contacts) <= 1:
            print("📭 No contacts to edit.")
            return

        # Find all contacts with matching name
        matches = []
        for idx, contact in enumerate(contacts, start=1):
            name = contact[0].strip().lower()
            if name == name_to_edit:
                matches.append((idx, contact))  # store row number and contact

        if not matches:
            print("❌ No contact found with that name.")
            return

        # If more than one match, ask user to choose
        print(f"\nFound {len(matches)} matching contact(s):")
        for i, (row, contact) in enumerate(matches, start=1):
            print(f"{i}. {contact[0]} | {contact[1]} | {contact[2]} | {contact[3]}")

        while True:
            try:
                selection = int(input("\nEnter the number of the contact to edit: "))
                if 1 <= selection <= len(matches):
                    break
                else:
                    print(f"Please enter a number between 1 and {len(matches)}.")
            except ValueError:
                print("Please enter a valid number.")

        # Edit the selected contact
        row_number, contact = matches[selection - 1]
        print()

        new_name = input(f"Name [{contact[0]}]: ").strip() or contact[0]
        new_phone = input(f"Phone [{contact[1]}]: ").strip() or contact[1]
        new_email = input(f"Email [{contact[2]}]: ").strip() or contact[2]
        new_notes = input(f"Notes [{contact[3]}]: ").strip() or contact[3]

        worksheet.update(f"A{row_number}:D{row_number}", [[new_name, new_phone, new_email, new_notes]])
        print("✅ Contact updated successfully.")

    except Exception as e:
        print("❌ Failed to edit contact.")
        print(f"Error: {e}")

def print_menu():
    print("\n==== FriendFinder Menu ====")
    print("1. Add Contact")
    print("2. View All Contacts")
    print("3. Search Contact by Name")
    print("4. Edit Contact")
    print("5. Exit")
   

def main():
    print("welcome to FriendFinder")
    print("This is a simple contact management system.")
    print("You can add, view, and search for contacts.")
    print("You can also update and delete contacts.")
    print("You can also search for contacts by name.")
    while True:
        print_menu()
        choice = input("Choose an option (1–5): ").strip()

        if choice == "1":
            add_contact()
        elif choice == "2":
            view_contacts()
        elif choice == "3":
            search_contact()
        elif choice == "4":
            edit_contact()
        elif choice == "5":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter a number from 1 to 5.")


if __name__ == "__main__":
    main()

