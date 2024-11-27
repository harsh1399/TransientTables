from constants import driver_path, brave_path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as BraveService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType

# Define Brave path
options = webdriver.ChromeOptions()
options.binary_location = brave_path

# Create new automated instance of Brave
driver = webdriver.Chrome(service=BraveService(ChromeDriverManager(chrome_type=ChromeType.BRAVE).install()),options = options)