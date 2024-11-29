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
                else:
                    secondary_links.append(base_url + category["href"])
        return secondary_links
    except Exception as e:
        print(e)
    

# Step 3: Main function
if __name__ == '__main__':
    # Scrape the product data
    # titleData = ["id","Store page link", "Product item page link", "Store_name", "Category", "Product_description", "Product Name", "Weight/Quantity", "Units/Counts", "Price", "image_file_names", "Image_Link", "Store Rating", "Store Review number", "Product Rating", "Product Review number", "Address", "Phone number", "Latitude", "Longitude", "Description Detail", "Nutrition & Info", "Halal Certification"]
    # widths = [10,50,50,60,45,70,35,25,25,20,130,130,30,30,30,30,60,50,60,60,80,80,80]
    # style = xlwt.easyxf('font: bold 1; align: horiz center')
    # products = []

    # if(not os.path.isdir("products")):
    #     os.mkdir("products")

    # now = datetime.now()
    # current_time = now.strftime("%m-%d-%Y-%H-%M-%S")
    # prefix = now.strftime("%Y%m%d%H%M%S%f_")
    # os.mkdir("products/"+current_time)
    # os.mkdir("products/"+current_time+"/images")
    
    
    # workbook = xlwt.Workbook()
    # sheet = workbook.add_sheet('Sheet1')

    # for col_index, value in enumerate(titleData):
    #     first_col = sheet.col(col_index)
    #     first_col.width = 256 * widths[col_index]  # 20 characters wide
    #     sheet.write(0, col_index, value, style)
        
    # for row_index, row in enumerate(records):
    #     for col_index, value in enumerate(row):
    #         sheet.write(row_index+1, col_index, value)

    # # Save the workbook
    # workbook.save("products/"+current_time+"/products.xls")
    cookies = get_cookies()
    print(cookies)
    departments = get_departments(cookies)
    secondaries = get_secondaries(cookies, departments)
    other_secondaries = get_categories(cookies, secondaries)
    secondaries1 = get_categories(cookies, other_secondaries)
    secondaries2 = get_categories(cookies, secondaries1)
    
    
    
    
