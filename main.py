import requests
import xlwt
import os
from datetime import datetime
import imghdr
from fake_useragent import UserAgent
from driver import CustomWebDriver
from selenium.webdriver.common.by import By

base_url = "https://www.samsclub.com"
products = []
section_id = 1

def get_departments(driver):
    global base_url
    ua = UserAgent()
    headers = {
        'User-Agent': ua.random
    }
    try:
        response = driver.get(base_url + "/c?xid=hdr:shop:moredepartments")
        # with open('index.html', 'w', encoding='utf-8') as file:
        #     file.write(response.text)
        links = driver.find_elements(By.CLASS_NAME, "bst-link bst-link-small bst-link-primary")
        # links = soup.find_all('a', class_="bst-link bst-link-small bst-link-primary")
        departments = []
        for link in links:
            if link.get_attribute("href").startswith('/c/'):
                departments.append(base_url + link.get_attribute("href"))
                print(link.get_attribute("href"))
        return departments
    except Exception as e:
        print(e)
        
def get_secondaries(driver, departments):
    global base_url
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
        }
        secondary_links = []
        for department in departments:
            driver.get(department, headers=headers, cookies=cookies)
            secondaries = driver.find_elements(By.CLASS_NAME, "bst-link bst-link-small bst-link-primary")
            for secondary in secondaries:
                if secondary.get_attribute("href").startswith('/c/'):
                    secondary_links.append(base_url + secondary.get_attribute("href"))
                    print(base_url + secondary.get_attribute("href"))
        return secondary_links
    except Exception as e:
        print(e)
        
def get_categories(driver, secondaries):
    global base_url
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
        }
        category_links = []
        secondary_links = []
        for secondary in secondaries:
            response = driver.get(secondary, headers=headers, cookies=cookies)
            categories = driver.find_elements(By.CLASS_NAME, "bst-link bst-link-small bst-link-primary")
            for category in categories:
                if category.get_attribute("href").startswith('/b/'):
                    category_links.append(base_url + category.get_attribute("href"))
                    href = category.get_attribute("href").split('?')[0]
                    print(base_url + href)
                elif category.get_attribute("href").startswith('/c/'):
                    secondary_links.append(base_url + category.get_attribute("href"))
        return secondary_links
    except Exception as e:
        print(e)
    

# Step 3: Main function
if __name__ == '__main__':
    driver = CustomWebDriver(is_eager=True)

    departments = get_departments(driver)
    secondaries = get_secondaries(driver, departments)
    other_secondaries = get_categories(driver, secondaries)
    if other_secondaries is not None:
        secondaries1 = get_categories(driver, other_secondaries)
    
    
    
    
