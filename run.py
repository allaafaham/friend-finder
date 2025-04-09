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

    
def view_contacts():
    print("\n--- All Contacts ---")
    try:
        worksheet = SHEET.sheet1
        contacts = worksheet.get_all_values()

        if len(contacts) <= 1:
            print("📭 No contacts found.")
            return

        # Optional: skip the header row if it exists
        for i, contact in enumerate(contacts, start=1):
            print(f"{i}. {contact[0]} | {contact[1]} | {contact[2]} | {contact[3]}")

    except Exception as e:
        print("❌ Failed to retrieve contacts.")
        print(f"Error: {e}")

if __name__ == "__main__":
    view_contacts()

