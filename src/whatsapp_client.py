import os
import sys
import threading
import time
import random
import subprocess
from PIL import Image
from selenium_stealth import stealth
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

try:
    from config import settings
    from src.utils.session_manager import save_session, load_session
    from src.utils.error_handlers import handle_error
    from src.utils.file_handlers import get_media_path
    print("[✓] Configuration and utilities imported successfully")
except ImportError as e:
    print(f"[×] Critical import error: {e}")
    raise

class WhatsAppClient:
    def __init__(self):
        self.driver = None
        self.running = True
        self.lock = threading.Lock()
        self.last_messages = {}
        self.setup_driver()
        self.login()
        self.start_message_monitor()
    # Existing methods remain unchanged...


    def setup_driver(self):
        """Configure Chrome WebDriver with desktop spoofing"""
        options = webdriver.ChromeOptions()
        
        # Desktop User-Agent (Updated Chrome 119)
        desktop_ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        options.add_argument(f"user-agent={desktop_ua}")
        
        # Desktop viewport configuration
        options.add_argument("--window-size=1920,1080")
        
        # Headless mode settings
        if settings.HEADLESS:
            options.add_argument("--headless=new")
            options.add_argument("--disable-blink-features=AutomationControlled")
        
        # Common options
        options.add_argument("--disable-notifications")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        service = Service(settings.PATHS['driver'])
        self.driver = webdriver.Chrome(service=service, options=options)
        
        # Stealth configuration
        stealth(
            self.driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            fix_hairline=True,
        )
        
        # WebDriver mask
        self.driver.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument", {
                "source": """
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined
                    });
                """
            }
        )

    def human_delay(self, min=0.5, max=2.0):
        """Randomized human delay system"""
        time.sleep(random.uniform(min, max))

    def login(self):
        """Desktop-optimized authentication flow"""
        try:
            # Force desktop version with URL parameter
            self.driver.get("https://web.whatsapp.com/?desktop")
            print("[•] Loading WhatsApp Desktop Web...")

            print("[!] Waiting for QR code...")
            qr_element = WebDriverWait(self.driver, settings.TIMEOUTS['qr_scan']).until(
                EC.presence_of_element_located((By.XPATH, "//canvas[@aria-label='Scan this QR code to link a device!']"))
            )
            
            self.display_terminal_qr_simple(qr_element)
            self.display_terminal_qr_advanced(qr_element)
            
            WebDriverWait(self.driver, settings.TIMEOUTS['qr_scan']).until(
                EC.invisibility_of_element_located((By.XPATH, "//canvas[@aria-label='Scan this QR code to link a device!']"))
            )
            print("\n[✓] Desktop authentication successful!")

            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, settings.XPATHS['new_chat']))
            )
            save_session(self.driver, settings.PATHS['cookies'])
            print("[✓] Desktop session saved")

        except TimeoutException as e:
            handle_error(f"Login timeout: {str(e)}", fatal=True)
        except Exception as e:
            handle_error(f"Login failed: {str(e)}", fatal=True)

    def try_restore_session(self):
        """Session restoration with desktop validation"""
        if not os.path.exists(settings.PATHS['cookies']):
            return False

        print("[•] Found existing session cookies")
        load_session(self.driver, settings.PATHS['cookies'])
        self.driver.get("https://web.whatsapp.com/?desktop")  # Reload desktop version
        
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@data-testid='chat-list-search']"))
            )
            print("[✓] Desktop session restored")
            return True
        except TimeoutException:
            print("[!] Session expired or mobile interface detected")
            os.remove(settings.PATHS['cookies'])
            return False

    # Existing methods below remain unchanged but benefit from new configurations
    # -------------------------------------------------------------------------

    def display_terminal_qr_simple(self, qr_element):
        """Simple approach: Save QR as image file"""
        try:
            qr_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'temp')
            os.makedirs(qr_dir, exist_ok=True)
            qr_path = os.path.join(qr_dir, 'whatsapp_qr.png')
            
            qr_element.screenshot(qr_path)
            
            print("\n[✓] QR CODE APPROACH 1:")
            print(f"[✓] QR Code saved as '{qr_path}'")
            print("[!] Please scan the QR code image with your WhatsApp mobile app")
            print("[!] Waiting for scan...\n")
        except Exception as e:
            print(f"[!] Error saving QR code: {e}")

    def display_terminal_qr_advanced(self, qr_element):
        """Advanced approach using zbarimg + qrencode"""
        try:
            print("[✓] QR CODE APPROACH 2:")
            temp_qr = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'temp', 'temp_qr.png')
            qr_element.screenshot(temp_qr)
            
            try:
                # Extract QR data using zbarimg
                result = subprocess.check_output(
                    ['zbarimg', '--quiet', '-Sdisable', '-Sqrcode.enable', temp_qr],
                    stderr=subprocess.STDOUT
                ).decode().strip()
                
                if not result.startswith('QR-Code:'):
                    raise ValueError("QR data not found")

                qr_data = result.split(':', 1)[1]
                
                # Generate terminal QR using qrencode
                print("\nTerminal QR Code (scan with WhatsApp):")
                subprocess.run(['qrencode', '-t', 'UTF8', '-o', '-', qr_data])
                print(f"\nQR Data: {qr_data}")
                print("[!] If terminal QR doesn't scan, use the saved image file")
                
            except Exception as e:
                print(f"[!] Error generating terminal QR: {e}")
                self.fallback_ascii_qr(temp_qr)
                
        except Exception as e:
            print(f"[!] Error rendering terminal QR: {e}")
            print("[!] Please use the saved QR code image instead")

    def fallback_ascii_qr(self, temp_qr):
        """Fallback to ASCII QR if system tools fail"""
        try:
            img = Image.open(temp_qr)
            img = img.resize((40, 40)).convert('L')
            pixels = list(img.getdata())
            
            ascii_chars = ' ░▒▓█'
            
            border = '╔' + '═' * 42 + '╗'
            print(f"\n{border}\n║ {'SCAN QR CODE':^40} ║")
            print('╟' + '─' * 42 + '╢')
            
            for i in range(0, len(pixels), img.width):
                line = '║ ' + ''.join([ascii_chars[min(p // 64, 4)] for p in pixels[i:i+img.width]]) + ' ║'
                print(line)
            
            print('╚' + '═' * 42 + '╝')
        except Exception as e:
            print("[!] All QR display methods failed - use saved image file")

    def send_message(self, number, message):
        """Desktop-optimized message sending"""
        with self.lock:
            try:
                self.driver.get(f"{settings.WHATSAPP_URL}/send?phone={number}&text={message}")
                self.human_delay(1, 2)
                
                send_btn = WebDriverWait(self.driver, settings.TIMEOUTS['element_wait']).until(
                    EC.element_to_be_clickable((By.XPATH, settings.XPATHS['send_button']))
                )
                ActionChains(self.driver)\
                    .move_to_element(send_btn)\
                    .pause(0.2)\
                    .click()\
                    .perform()
                return True
            except Exception as e:
                handle_error(f"Message failed: {str(e)}")
                return False

    def send_file(self, number, file_path, caption=""):
        """Desktop file upload flow"""
        with self.lock:
            try:
                self.driver.get(f"{settings.WHATSAPP_URL}/send?phone={number}")
                self.human_delay(1, 2)
                
                WebDriverWait(self.driver, settings.TIMEOUTS['element_wait']).until(
                    EC.element_to_be_clickable((By.XPATH, settings.XPATHS['attach_button']))
                ).click()
                
                file_input = WebDriverWait(self.driver, settings.TIMEOUTS['element_wait']).until(
                    EC.presence_of_element_located((By.XPATH, settings.XPATHS['file_input']))
                )
                file_input.send_keys(get_media_path(file_path, 'upload'))
                
                if caption:
                    WebDriverWait(self.driver, settings.TIMEOUTS['element_wait']).until(
                        EC.presence_of_element_located((By.XPATH, settings.XPATHS['caption_box']))
                    ).send_keys(caption)
                    
                WebDriverWait(self.driver, settings.TIMEOUTS['file_upload']).until(
                    EC.element_to_be_clickable((By.XPATH, settings.XPATHS['send_button']))
                ).click()
                return True
            except Exception as e:
                handle_error(f"File send failed: {str(e)}")
                return False
    def view_messages(self, contact_name_or_number):
                    """View messages with timestamp and sender information."""
                    with self.lock:
                        try:
                            # Open the chat for the specified contact
                            self.driver.get(f"{settings.WHATSAPP_URL}/send?phone={contact_name_or_number}")
                            self.human_delay(1, 2)
                
                            # Wait for the chat to load
                            WebDriverWait(self.driver, settings.TIMEOUTS['element_wait']).until(
                                EC.presence_of_element_located((By.XPATH, settings.XPATHS['chat_container']))
                            )
                            time.sleep(2)  # Allow messages to load
                
                            # Extract messages with their metadata
                            message_elements = self.driver.find_elements(By.XPATH, "//div[@class='copyable-text']")
                            print(f"\nMessages with {contact_name_or_number}:")
                
                            for message in message_elements:
                                # Extract the timestamp and sender name from the attribute
                                metadata = message.get_attribute("data-pre-plain-text")
                                # Extract the message text
                                message_text = message.find_element(By.XPATH, ".//span[@class='_ao3e selectable-text copyable-text']").text
                
                                # Print the metadata and message
                                print(f"  {metadata}{message_text}")
                
                            return True
                
                        except Exception as e:
                            handle_error(f"Failed to view messages: {str(e)}")
                            return False
    def monitor_messages(self):
        """Background monitoring (unchanged)"""
        while self.running:
            try:
                pass  # Implementation here
            except Exception as e:
                handle_error(f"Monitoring error: {str(e)}")
            time.sleep(settings.POLL_INTERVAL)

    def start_message_monitor(self):
        """Start monitor thread (unchanged)"""
        monitor_thread = threading.Thread(target=self.monitor_messages)
        monitor_thread.daemon = True
        monitor_thread.start()

    def cleanup(self):
        """Cleanup (unchanged)"""
        self.running = False
        if self.driver:
            self.driver.quit()
            print("[✓] Browser session closed")
