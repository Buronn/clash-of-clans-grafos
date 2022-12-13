from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import set_chrome_options
import pandas as pd

def check_column(column):
    '''Check if the column is a bad column'''
    BAD_COLUMNS = ["Single Mode", "Multi Mode"]
    if column in BAD_COLUMNS:
        return False
    else:
        return True

def text_to_int(str):
    '''Convert a string with a "," to an int'''
    return (str.replace(',', ''))

if "__main__" == __name__:
    # Start Selenium
    print("Selenium Version: "+str(webdriver.__version__))
    MAIN_URL = "https://www.clashtrack.com/en/wiki"
    driver = webdriver.Chrome(options=set_chrome_options())
    driver.set_window_size(1024, 768)
    driver.get(MAIN_URL)
    driver.implicitly_wait(10)
    # Print all h3 tags
    h3_tags = driver.find_elements(by=By.TAG_NAME, value="h3")
    # Create a list of h3 tags
    h3_tags_list = []
    for h3_tag in h3_tags:
        h3_tags_list.append(h3_tag.text)
    driver.close()
    title_index = 0
    json_output = {}
    df = pd.DataFrame()
    # Empty list

    #h3_tags_list = []
    #h3_tags_list.append("Inferno Tower")

    # Get all h3 tags
    for h3_tag in h3_tags_list:
        if h3_tag == "Town Hall":
            driver.close()
            break
        
        print("h3_tag: "+h3_tag)
        level_index = 0
        if h3_tag == "Spring Traps":
            h3_tag = "Spring Trap"
        if h3_tag == "The Headhunter":
            h3_tag = "Headhunter"
        driver = webdriver.Chrome(options=set_chrome_options())
        driver.set_window_size(1920, 1080)
        driver.get(MAIN_URL+"/"+h3_tag.replace(" ", "_"))
        #table = driver.find_element(by=By.XPATH, value="//table[@class='table table-striped table-hover text-center']")
        table = driver.find_element(by=By.TAG_NAME, value="table")
        headers = table.find_element(by=By.TAG_NAME, value="thead")
        headers = headers.find_elements(by=By.TAG_NAME, value="th")
        headers_list = []
        level = False
        
        # Get all headers and append them to a list
        for header in headers:
            if check_column(header.text):
                if header.find_elements(by=By.TAG_NAME, value="span"):
                    headers_list.append(text_to_int(header.text)+" "+header.find_element(by=By.TAG_NAME, value="span").get_attribute("class"))
                else:
                    headers_list.append(header.text)
        print(headers_list)
        rows = table.find_element(by=By.TAG_NAME, value="tbody")
        rows = rows.find_elements(by=By.TAG_NAME, value="tr")
        all_cells = []

        # Get all cells and append them to a list
        for row in rows:
            row = row.find_elements(by=By.TAG_NAME, value="td")
            cells_list = []
            for cell in row:
                # if element has span inside, get the class of the span
                if cell.find_elements(by=By.TAG_NAME, value="span"):
                    cells_list.append(text_to_int(cell.text)+" "+cell.find_element(by=By.TAG_NAME, value="span").get_attribute("class"))
                else:
                    cells_list.append(text_to_int(cell.text))
            all_cells.append(cells_list)
            print(cells_list)
            level_index += 1

        # Close the driver
        driver.close()
        title_index += 1
        # Create a dataframe and save it to a csv file
        df = pd.DataFrame(all_cells, columns=headers_list)
        df.to_csv("output2/"+h3_tag.replace(" ", "_")+".csv", index=False)
