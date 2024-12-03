import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# Specify the path to the ChromeDriver
s = Service(r'C:\Users\m.krushovski\.cache\selenium\chromedriver\win64\131.0.6778.85\chromedriver.exe')

chromeOptions = Options()
chromeOptions.headless = False  # Set to True for headless operation
driver = webdriver.Chrome(service=s, options=chromeOptions)


def scroll_to_end_and_save_to_file():
    driver.get('https://taxireg.infosys.bg/pub/register')
    print('Starting driver...')
    time.sleep(3)  # Wait for page to load

    try:
        scrollable_element = driver.find_element(By.CSS_SELECTOR, 'mat-sidenav-content')
        print("Found scrollable element.")

        last_scroll_height = 0
        retries = 5

        with open("eik_data.txt", "w", encoding="utf-8") as file:
            written_eik = set()  # Keep track of already written ЕИК values to avoid duplicates

            while retries > 0:
                # Scroll down the container
                driver.execute_script("arguments[0].scrollBy(0, arguments[0].offsetHeight);", scrollable_element)
                time.sleep(0.4)  # Wait for content to load

                # Get the current scroll position
                current_scroll_height = driver.execute_script("return arguments[0].scrollTop;", scrollable_element)

                # Check if the content is still loading
                if current_scroll_height == last_scroll_height:
                    retries -= 1
                else:
                    retries = 5  # Reset retries if new content loads

                last_scroll_height = current_scroll_height

                # Extract the EIK values and save them
                elements = driver.find_elements(By.XPATH, "//span[contains(text(), 'ЕИК')]")
                for el in elements:
                    eik = el.text.strip()
                    eik_code = eik.replace('ЕИК', '').strip()
                    if eik not in written_eik:  # Avoid writing duplicates
                        file.write(f"{eik_code},")  # Write to file separated by commas
                        written_eik.add(eik)

        print(f"ЕИК values saved to eik_data.txt.")

    except Exception as e:
        print(f"Error during scrolling: {e}")


try:
    scroll_to_end_and_save_to_file()
finally:
    print('Press Enter to close the browser...')
    input()
    driver.quit()
