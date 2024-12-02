import requests
from bs4 import BeautifulSoup
import xlwt
import os
from datetime import datetime
import imghdr
from fake_useragent import UserAgent

base_url = "https://www.samsclub.com"
products = []
section_id = 1

def get_cookies():
    try:
        data = {
            "visits": [{
                "AsmtCounted": [],
                "Data": {
                    "7123992": {
                        "Hits": 1
                    }
                }
            }]
        }
        headers = {'Content-Type': 'application/json'}

        response = requests.post("https://www.samsclub.com/__ssobj/api", json=data, headers=headers)
        data = response.json()
        return data["cookies"]
    except Exception as e:
        print(e)

def get_departments(cookies):
    global base_url
    ua = UserAgent()
    headers = {
        'User-Agent': ua.random
    }
    try:
        response = requests.get(base_url + "/c?xid=hdr:shop:moredepartments", headers=headers, cookies=cookies)
        soup = BeautifulSoup(response.text, 'html.parser')
        # with open('index.html', 'w', encoding='utf-8') as file:
        #     file.write(response.text)
        links = soup.find_all('a', class_="bst-link bst-link-small bst-link-primary")
        departments = []
        for link in links:
            if link["href"].startswith('/c/'):
                departments.append(base_url + link["href"])
                print(link["href"])
        return departments
    except Exception as e:
        print(e)
        
def get_secondaries(cookies, departments):
    global base_url
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
        }
        secondary_links = []
        for department in departments:
            response = requests.get(department, headers=headers, cookies=cookies)
            soup = BeautifulSoup(response.text, 'html.parser')
            secondaries = soup.find_all('a', class_="bst-link bst-link-small bst-link-primary")
            for secondary in secondaries:
                if secondary["href"].startswith('/c/'):
                    secondary_links.append(base_url + secondary["href"])
                    print(base_url + secondary["href"])
        return secondary_links
    except Exception as e:
        print(e)
        
def get_categories(cookies, secondaries):
    global base_url
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
        }
        category_links = []
        secondary_links = []
        for secondary in secondaries:
            response = requests.get(secondary, headers=headers, cookies=cookies)
            soup = BeautifulSoup(response.text, 'html.parser')
            categories = soup.find_all('a', class_="bst-link bst-link-small bst-link-primary")
            for category in categories:
                if category["href"].startswith('/b/'):
                    category_links.append(base_url + category["href"])
                    category["href"] = category["href"].split('?')[0]
                    print(base_url + category["href"])
                elif category["href"].startswith('/c/'):
                    secondary_links.append(base_url + category["href"])
        return secondary_links
    except Exception as e:
        print(e)
    

# Step 3: Main function
if __name__ == '__main__':
    cookies = get_cookies()
    departments = get_departments(cookies)
    secondaries = get_secondaries(cookies, departments)
    other_secondaries = get_categories(cookies, secondaries)
    secondaries1 = get_categories(cookies, other_secondaries)
    
    
    
    
