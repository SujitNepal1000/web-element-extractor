from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
import pandas as pd
from bs4 import BeautifulSoup
import time

class TestRunner:
    def __init__(self):
        self.driver = None

    def start_browser(self, url):
        options = webdriver.ChromeOptions()
        # Add headless option if needed
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        try:
            # Initialize Chrome browser
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            self.driver.maximize_window()
            self.driver.get(url)
            time.sleep(2)  # Wait for page load
        except Exception as e:
            print(f"Error starting browser: {e}")

    def enter_value(self, locator, value):
        if self.driver:
            try:
                element = self.driver.find_element(By.XPATH, locator)
                element.clear()
                element.send_keys(value)
                time.sleep(1)
            except Exception as e:
                print(f"Error entering value: {e}")
        else:
            print("Browser is not initialized. Call start_browser() first.")

    def click_element(self, locator):
        if self.driver:
            try:
                element = self.driver.find_element(By.XPATH, locator)
                ActionChains(self.driver).move_to_element(element).click().perform()
                time.sleep(3)
            except Exception as e:
                print(f"Error clicking element: {e}")
        else:
            print("Browser is not initialized. Call start_browser() first.")

    def scroll_to_element(self, locator):
        if self.driver:
            try:
                element = self.driver.find_element(By.XPATH, locator)
                self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                time.sleep(1)
            except Exception as e:
                print(f"Error scrolling to element: {e}")
        else:
            print("Browser is not initialized. Call start_browser() first.")

    def verify_element(self, locator):
        if self.driver:
            try:
                element = self.driver.find_element(By.XPATH, locator)
                assert element.is_displayed(), f"Element with locator {locator} is not displayed."
            except Exception as e:
                print(f"Error verifying element: {e}")
        else:
            print("Browser is not initialized. Call start_browser() first.")

    def get_page_source(self):
        if self.driver:
            return self.driver.page_source
        else:
            print("Browser is not initialized. Call start_browser() first.")
            return None

    def extract_locators(self, html_content):
        if not html_content:
            print("No HTML content provided for locator extraction.")
            return pd.DataFrame()

        soup = BeautifulSoup(html_content, "html.parser")
        elements = []

        def add_element(name, tag, attrs, text=None, placeholder=None):
            element_data = {
                "Name": text if text else (placeholder if placeholder else name),
                "XPath": '',
                "ID": '',
                "Class": '',
                "CSS Selector": '',
                "Full Link": '',
                "Partial Link": ''
            }

            if tag == 'input':
                if 'id' in attrs:
                    element_data["XPath"] = f"//input[@id='{attrs['id']}']"
                elif 'placeholder' in attrs:
                    element_data["XPath"] = f"//input[@placeholder='{attrs['placeholder']}']"
                elif 'name' in attrs:
                    element_data["XPath"] = f"//input[@name='{attrs['name']}']"
                elif 'class' in attrs:
                    class_name = ' '.join(attrs['class'])
                    element_data["XPath"] = f"//input[@class='{class_name}']"
                else:
                    element_data["XPath"] = "//input"
            
            elif tag == 'div':
                button = element.find('button', text=True)  
                if button:
                    button_text = button.get_text(strip=True)
                    element_data["XPath"] = f"//div/button[normalize-space(text())='{button_text}']"
                    element_data["Name"] = f"div containing button = text ({button_text})"
                elif 'id' in attrs:
                    element_data["XPath"] = f"//div[@id='{attrs['id']}']"
                    element_data["Name"] = f"div = id ({attrs['id']})"
                elif 'class' in attrs:
                    class_name = ' '.join(attrs['class'])
                    element_data["XPath"] = f"//div[@class='{class_name}']"
                    element_data["Name"] = f"div = class"
                else:
                    element_data["XPath"] = "//div"
                    element_data["Name"] = "div"

            elif tag == 'button':
                if text and len(text.strip()) > 0:
                    element_data["XPath"] = f"//button[text()='{text.strip()}']"
                    element_data["Name"] = f"button = text ({text.strip()})"
                elif 'id' in attrs:
                    element_data["XPath"] = f"//button[@id='{attrs['id']}']"
                    element_data["Name"] = f"button = id ({attrs['id']})"
                elif 'class' in attrs:
                    class_name = ' '.join(attrs['class'])
                    element_data["XPath"] = f"//button[@class='{class_name}']"
                    element_data["Name"] = f"button = class"
                elif 'type' in attrs:
                    element_data["XPath"] = f"//button[@type='{attrs['type']}']"
                    element_data["Name"] = f"button = type ({attrs['type']})"
                else:
                    element_data["XPath"] = "//button"
                    element_data["Name"] = "button"

            elif tag == 'a':
                if 'href' in attrs:
                    element_data["XPath"] = f"//a[@href='{attrs['href']}']"
                    element_data["Name"] = f"link = href ({attrs['href']})"
                elif text and len(text.strip()) > 0:
                    element_data["XPath"] = f"//a[normalize-space(text())='{text.strip()}']"
                    element_data["Name"] = f"link = text ({text.strip()})"
                else:
                    element_data["XPath"] = "//a"
                    element_data["Name"] = "link"

            elif tag == 'span':
                # Give priority to text extraction for spans
                if text and len(text.strip()) > 0:
                    element_data["XPath"] = f"//span[normalize-space(text())='{text.strip()}']"
                    element_data["Name"] = f"span = text ({text.strip()})"
                elif 'id' in attrs:
                    element_data["XPath"] = f"//span[@id='{attrs['id']}']"
                    element_data["Name"] = f"span = id ({attrs['id']})"
                elif 'class' in attrs:
                    class_name = ' '.join(attrs['class'])
                    element_data["XPath"] = f"//span[@class='{class_name}']"
                    element_data["Name"] = f"span = class"
                else:
                    element_data["XPath"] = "//span"
                    element_data["Name"] = "span"

            if 'id' in attrs:
                element_data["ID"] = attrs["id"]
            if 'class' in attrs:
                element_data["Class"] = ' '.join(attrs['class'])
            if tag:
                element_data["CSS Selector"] = tag

            if 'href' in attrs:
                element_data["Full Link"] = attrs['href']
                element_data["Partial Link"] = attrs['href'].split('/')[-1]

            elements.append(element_data)

        keywords = {
            "button": "Button",
            "a": "Link",
            "input": "Input/Field",
            "textarea": "Text Area",
            "select": "Dropdown",
            "h1": "Heading 1",
            "h2": "Heading 2",
            "h3": "Heading 3",
            "h4": "Heading 4",
            "h5": "Heading 5",
            "h6": "Heading 6",
            "label": "Label",
            "card": "Card",
            "filter": "Filter",
            "div": "Div",
            "span": "Span"
        }

        for tag, name in keywords.items():
            for element in soup.find_all(tag):
                attrs = element.attrs
                if tag == "a" and element.get_text(strip=True):
                    add_element(name, tag, attrs, text=element.get_text(strip=True))
                elif tag == "button" and element.get_text(strip=True):
                    add_element(name, tag, attrs, text=element.get_text(strip=True))
                elif tag.startswith("h") and element.get_text(strip=True):
                    add_element(name, tag, attrs, text=element.get_text(strip=True))
                elif tag == "input" and 'placeholder' in attrs:
                    add_element(name, tag, attrs, placeholder=attrs['placeholder'])
                elif tag == "label":
                    add_element(name, tag, attrs, text=element.get_text(strip=True))
                elif tag in ["span", "div"] and element.get_text(strip=True):
                    add_element(name, tag, attrs, text=element.get_text(strip=True))

        df = pd.DataFrame(elements)
        df.index += 1
        return df

    def save_locators_to_file(self, filename):
        html_content = self.get_page_source()
        df = self.extract_locators(html_content)
        df.index.name = 'S.N'
        df = df[["Name", "ID", "Class", "XPath", "CSS Selector", "Full Link", "Partial Link"]]
        df.to_csv(filename, index=True)
        print(f"Locators saved to {filename}")

    def stop_browser(self):
        if self.driver:
            self.driver.quit()
            self.driver = None
            print("Browser closed.")

# Usage Example
test_runner = TestRunner()
test_runner.start_browser("https://example.com")  # Start the browser with your desired URL
test_runner.save_locators_to_file("locators.csv")
test_runner.stop_browser()  # Close the browser when done
