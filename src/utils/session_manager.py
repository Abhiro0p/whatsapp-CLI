import pickle
import os

def save_session(driver, path):
    cookies = driver.get_cookies()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as file:
        pickle.dump(cookies, file)

def load_session(driver, path):
    with open(path, 'rb') as file:
        cookies = pickle.load(file)
        for cookie in cookies:
            driver.add_cookie(cookie)
