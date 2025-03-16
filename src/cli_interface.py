from src.whatsapp_client import WhatsAppClient
from src.utils.file_handlers import validate_file_path
import readline
import json
import os
import vobject  # For parsing and creating .vcf files

class ContactManager:
    def __init__(self):
        self.contacts_file = os.path.expanduser("~/.whatsapp_contacts.json")
        self.contacts = self._load_contacts()

    def _load_contacts(self):
        if os.path.exists(self.contacts_file):
            with open(self.contacts_file, 'r') as f:
                return json.load(f)
        return {}

    def _save_contacts(self):
        with open(self.contacts_file, 'w') as f:
            json.dump(self.contacts, f, indent=2)

    def add_contact(self, name, number):
        self.contacts[name.lower()] = number
        self._save_contacts()

    def get_number(self, input_str):
        return self.contacts.get(input_str.lower(), input_str)

    def list_contacts(self):
        return self.contacts.items()

    def delete_contact(self, name):
        """Delete a contact by name."""
        name = name.lower()
        if name in self.contacts:
            del self.contacts[name]
            self._save_contacts()
            return True
        return False

    def import_contacts_from_vcf(self, vcf_file_path):
        """Import contacts from a .vcf file."""
        if not os.path.exists(vcf_file_path):
            print(f"✗ File '{vcf_file_path}' not found.")
            return False

        try:
            with open(vcf_file_path, 'r', encoding='utf-8') as f:
                vcf_data = f.read()

            # Parse the .vcf file
            vcard_list = vobject.readComponents(vcf_data)
            imported_count = 0

            for vcard in vcard_list:
                try:
                    name = vcard.fn.value
                    number = None

                    # Extract the first phone number
                    if hasattr(vcard, 'tel'):
                        number = vcard.tel.value
                        if number.startswith('+'):
                            number = number.replace(' ', '')  # Normalize the number

                    if name and number:
                        self.add_contact(name, number)
                        imported_count += 1
                except Exception as e:
                    print(f"✗ Error processing contact: {e}")
                    continue

            print(f"✓ Imported {imported_count} contacts from '{vcf_file_path}'.")
            return True

        except Exception as e:
            print(f"✗ Error reading .vcf file: {e}")
            return False

    def export_contacts_to_vcf(self, vcf_file_path):
        """Export contacts to a .vcf file."""
        try:
            with open(vcf_file_path, 'w', encoding='utf-8') as f:
                for name, number in self.contacts.items():
                    # Create a vCard object
                    vcard = vobject.vCard()
                    vcard.add('fn').value = name  # Full name
                    vcard.add('tel').value = number  # Phone number
                    f.write(vcard.serialize())
                    f.write("\n")  # Add a newline between vCards

            print(f"✓ Exported {len(self.contacts)} contacts to '{vcf_file_path}'.")
            return True

        except Exception as e:
            print(f"✗ Error exporting contacts: {e}")
            return False

class CLIInterface:
    def __init__(self):
        self.client = WhatsAppClient()
        self.contacts = ContactManager()
        
    def start(self):
        try:
            while True:
                cmd = input("\nCommand [send/attach/add/list/delete/import/export/view/exit]: ").strip().lower()
                
                if cmd == "send":
                    self.handle_message()
                elif cmd == "attach":
                    self.handle_attachment()
                elif cmd == "add":
                    self.handle_add_contact()
                elif cmd == "list":
                    self.handle_list_contacts()
                elif cmd == "delete":
                    self.handle_delete_contact()
                elif cmd == "import":
                    self.handle_import_contacts()
                elif cmd == "export":
                    self.handle_export_contacts()
                elif cmd == "view":
                    self.handle_view_messages()
                elif cmd == "exit":
                    break
                    
        finally:
            self.client.cleanup()

    def handle_message(self):
        identifier = input("Contact name or phone number (+format): ").strip()
        number = self.contacts.get_number(identifier)
        message = input("Message: ").strip()
        if self.client.send_message(number, message):
            print("✓ Message sent")

    def handle_attachment(self):
        identifier = input("Contact name or phone number (+format): ").strip()
        number = self.contacts.get_number(identifier)
        file_path = input("File path: ").strip()
        if validate_file_path(file_path):
            caption = input("Caption (optional): ").strip()
            if self.client.send_file(number, file_path, caption):
                print("✓ File sent")

    def handle_add_contact(self):
        name = input("Contact name: ").strip()
        number = input("Phone number (+country code): ").strip()
        self.contacts.add_contact(name, number)
        print(f"✓ Contact '{name}' added")

    def handle_list_contacts(self):
        print("\nSaved Contacts:")
        for name, number in self.contacts.list_contacts():
            print(f"  {name.title()}: {number}")
        print()

    def handle_delete_contact(self):
        """Handle the deletion of a contact."""
        name = input("Enter the name of the contact to delete: ").strip()
        if self.contacts.delete_contact(name):
            print(f"✓ Contact '{name}' deleted")
        else:
            print(f"✗ Contact '{name}' not found")

    def handle_import_contacts(self):
        """Handle importing contacts from a .vcf file."""
        vcf_file_path = input("Enter the path to the .vcf file: ").strip()
        self.contacts.import_contacts_from_vcf(vcf_file_path)

    def handle_export_contacts(self):
        """Handle exporting contacts to a .vcf file."""
        vcf_file_path = input("Enter the path to save the .vcf file: ").strip()
        self.contacts.export_contacts_to_vcf(vcf_file_path)

    def handle_view_messages(self):
        """Handle viewing messages for a contact."""
        identifier = input("Enter contact name or phone number (+format): ").strip()
        number = self.contacts.get_number(identifier)
        if self.client.view_messages(number):
            print("✓ Messages displayed")
        else:
            print("✗ Failed to view messages")

if __name__ == "__main__":
    interface = CLIInterface()
    interface.start()
