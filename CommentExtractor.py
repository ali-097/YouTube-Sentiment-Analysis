from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import csv
import re


def ScrapComment(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=ChromeService(
        ChromeDriverManager().install()), options=options)
    driver.get(url)
    prev_h = 0
    while True:
        height = driver.execute_script("""
                function getActualHeight() {
                    return Math.max(
                        Math.max(document.body.scrollHeight, document.documentElement.scrollHeight),
                        Math.max(document.body.offsetHeight, document.documentElement.offsetHeight),
                        Math.max(document.body.clientHeight, document.documentElement.clientHeight)
                    );
                }
                return getActualHeight();
            """)
        driver.execute_script(f"window.scrollTo({prev_h},{prev_h + 200})")
        time.sleep(1)
        prev_h += 200
        if prev_h >= height:
            break
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    title_text_div = soup.select_one('#container h1')
    title = title_text_div and title_text_div.text

    comment_div = soup.select("#content #content-text")
    comment_list = [x.text for x in comment_div]

    # Save comments to CSV file
    save_to_csv(title, comment_list)


def save_to_csv(title, comments):
    # Replace invalid characters with underscores
    title = re.sub(r'[\\/*?:"<>|]', '_', title)

    # Create the CSV file
    file_name = "comments.csv"
    with open(file_name, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Comment"])
        csv_writer.writerows([[comment] for comment in comments])


if __name__ == "__main__":
    url = input("Enter the URL of the YouTube video: ")
    ScrapComment(url)
