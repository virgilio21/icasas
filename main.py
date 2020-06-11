from selenium import webdriver
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

all_departments = []

class Department():
  price = ''
  title = ''
  bethrooms = ''
  bathrooms = None
  area = ''
  description = ''
  url = ''

def search_departments( location ):
  xpath_rent_option = '/html[1]/body[1]/div[6]/section[1]/div[4]/div[1]/div[2]/ul[1]/li[2]'
  rent_option = driver.find_element(By.XPATH, xpath_rent_option)
  rent_option.click()
  time.sleep(2)
  search_field = driver.find_element(By.ID, 'location-input')
  search_field.click()
  time.sleep(2)
  search_field.send_keys(location)
  time.sleep(3)
  first_option_wanted = driver.find_element(By.CLASS_NAME, 'tt-dropdown-menu')
  first_option_wanted.click()
  search_button = driver.find_element(By.ID, 'submitForm')
  search_button.click()

def print_departments( departments_list ):
  count = 0
  for current_deparment in departments_list:
    print(count)
    print(current_deparment.price)
    print(current_deparment.title)
    print(current_deparment.bethrooms)
    print(current_deparment.bathrooms)
    print(current_deparment.area)
    print(current_deparment.description)
    print(current_deparment.url)
    count +=1

def get_departments( driver_navegator):

  html = urlopen(driver_navegator.current_url)
  bs = BeautifulSoup(html.read(), 'html.parser')
  list_departmetns = bs.find_all('li',{'class':'ad'})
  return list_departmetns


if __name__ == "__main__":
  options = webdriver.ChromeOptions()
  options.add_argument("--start-maximized")
  driver = webdriver.Chrome(executable_path='/home/virgo/bin/chromedriver',chrome_options=options)

  driver.get("https://www.icasas.mx/")
  time.sleep(6)
  search_departments('Ciudad de mexico')
  time.sleep(6)

  print("Empezando obtencion de datos\n")
  is_live = True
  while is_live:
    bs_departments = get_departments(driver)
    for department in bs_departments:
      department_item = Department()
      department_item.bethrooms = department.select_one('span.rooms').get_text()
      price = department.select_one('div.price')
      department_item.price = price.get_text().replace("Desde",'').replace('MX$', '').strip()
      department_item.title = department.select_one('a.detail-redirection').get_text()
      department_item.url = department.select_one('a.detail-redirection')['href']
      department_item.area = department.select_one('span.areaBuilt').get_text().replace('m2', '')
      department_item.description = department.select_one('p.description').get_text()
      bathroom = department.select_one('span.bathrooms')
      department_item.bathrooms = bathroom.get_text().strip() if bathroom else 0 
      all_departments.append(department_item)    

    try:
      next_button = driver.find_element_by_css_selector('li.next > span')
      next_button.click()
      time.sleep(6)
    except:
      is_live = False
  
  print_departments( all_departments )
  print("\nobtencion de datos terminada")
  driver.close()