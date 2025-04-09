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


if __name__ == "__main__":
    search_contact()

