from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time


class Scrolling:
    def __init__(self):
        self.page_soup = ""

    def scroll(self, url):
        service = ChromeService(executable_path=ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
        driver.get(f"{url}")
        time.sleep(2)  # Allow 2 seconds for the web page to open
        scroll_pause_time = 10  # You can set your own pause time. My laptop is a bit slow so I use 1 sec

        i = 2
        temp = 0
        while True:
            scroll_height = driver.execute_script(
                "return document.body.scrollHeight;")  # Get two times scrollHeight (to fast scroll down)
            # Scroll one scroll height each time
            driver.execute_script("window.scrollTo(0, {scroll_height});".format(scroll_height=scroll_height))
            # Add 1 sec for each 10 scroll
            if i % 10 == 1:
                scroll_pause_time += 1

            time.sleep(scroll_pause_time)
            i += 1

            # Get all new item from scrolling down (this case for travelio.com)
            self.page_soup = BeautifulSoup(driver.page_source, "html.parser")
            items = self.page_soup.find_all("div", class_="property-box")

            # Break the loop
            if (len(items)) == temp:
                break
            temp = len(items)

        driver.close()
