# WhatsApp CLI

A command-line interface (CLI) for sending and managing WhatsApp messages using Selenium and Python.

## Features

- **Send Messages**: Send text messages to contacts.
- **Send Attachments**: Send files (images, documents, etc.) with optional captions.
- **Contact Management**:
  - Add, list, and delete contacts.
  - Import/export contacts in `.vcf` (vCard) format.
- **View Messages**: View chat history with a specific contact.
- **Session Persistence**: Save and restore WhatsApp sessions using cookies.

## Installation

### Prerequisites

1. **Python 3.8+**: Ensure Python is installed on your system.
2. **ChromeDriver**: Download and install ChromeDriver from [here](https://sites.google.com/chromium.org/driver/).
3. **Dependencies**: Install the required Python packages.

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/Abhiro0p/whatsapp-cli.git
   cd whatsapp-cli
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
3. Configure ChromeDriver:
- Ensure ChromeDriver is installed and its path is correctly set in config/settings.py
- Chrome and ChromeDriver should be of the same version
4. Run
  ```bash
  python -m src.cli_interface
