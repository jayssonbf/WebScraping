from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

"""
Basic overview of selenium over BeautifulSoup for web scrapping.
"""

if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.get('https://fgcuathletics.com/sports/womens-soccer/stats?path=wsoc')
    assert "Page not found" not in driver.page_source

    elem = driver.find_element(By.XPATH, "//*[@id='ui-id-3']")  # find Game-By-Game tab
    elem.send_keys(Keys.ENTER)  # access Game-By-Game tab

    """
    Explicit Waits - is a code you define to wait for a certain condition to occur before proceeding
    further in the code. It waits 10secs until it goes to the next page or tab 
    """
    try:
        table_head = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//*[@id='DataTables_Table_4']/thead/tr/th"))
        )
        # ---------------COLUMNS------------------
        columns = []
        for head in table_head:
            columns.append(head.text)
        print(f'{columns}')

        # ----------------ROWS-------------------
        table_rowData = driver.find_elements(By.XPATH, "//*[@id='DataTables_Table_4']/tbody/tr/td")
        rows = []

        for row in table_rowData:
            rows.append(re.sub('\\n'," ", row.text))

        print(f'{rows}')

    except:
        driver.quit()
