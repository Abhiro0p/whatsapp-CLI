import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

XPATHS = {
    'new_chat': '//button[@title="New chat"]',
    'send_button': '//span[@data-icon="send"]',
    'attach_button': '//span[@data-icon="plus"]',
    'file_input': '//input[@type="file"]',
    'caption_box': '//p[@class="selectable-text copyable-text x15bjb6t x1n2onr6"]',
    'chat_container': "//div[@class='x1n2onr6 x1vjfegm x1cqoux5 x14yy4lh']",  # Container for chat messages
    'message_elements': "//div[@class='_akbu']"
}

TIMEOUTS = {
    'qr_scan': 60,  # Increase to 60 seconds
    'element_wait': 60,
    'file_upload': 60
}

PATHS = {
    'driver': '/usr/bin/chromedriver',  # Path to ChromeDriver
    'cookies': os.path.join(BASE_DIR, 'sessions/cookies.pkl'),  # Cookie path
    'media_upload': os.path.join(BASE_DIR, 'media/uploads'),
    'media_download': os.path.join(BASE_DIR, 'media/downloads'),
    'logs': os.path.join(BASE_DIR, 'logs')
}

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/91.0.4472.124 Safari/537.36"
WHATSAPP_URL = "https://web.whatsapp.com"
POLL_INTERVAL = 5
HEADLESS = True
