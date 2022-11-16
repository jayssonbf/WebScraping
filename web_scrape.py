from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
import re

"""
Basic overview of selenium over BeautifulSoup for web scrapping.
"""

if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.get('https://fgcuathletics.com/sports/womens-soccer/stats?path=wsoc')
    assert "Page not found" not in driver.page_source

    for i in range(1, 4):

        try:
            # explicitly waits for the page to load to select the year
            selects = Select(WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//select"))
            ))
            selects.select_by_index(i)

            # explicitly waits for the page to load to click on the "Game-By-Game" tab
            tab = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='ui-id-3']"))
            )
            tab.send_keys(Keys.ENTER)  # access Game-By-Game tab

            """
            Explicit Waits - is a code you define to wait for a certain condition to occur before proceeding
            further in the code. It waits 10secs until it goes to the next page or tab
            """

            table_head = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//*[@id='DataTables_Table_4']/thead/tr/th"))
            )

            year = driver.find_element(By.XPATH, "//*[@id='main-content']/article/h1")
            year = "".join(re.findall('[\d]+', year.text))
            print(f'Year {year}')

            # ---------------COLUMNS------------------
            columns = []
            for head in table_head:
                columns.append(head.text)
            print(f'{columns}')

            # ----------------ROWS-------------------
            table_rowData = driver.find_elements(By.XPATH, "//*[@id='DataTables_Table_4']/tbody/tr")
            rows = []

            for row in table_rowData:
                rows.append(re.sub('\\n'," ", row.text))

            for n, row in enumerate(rows):
                print(f'Row {n+1}: {row}')
            print("")

        except:
            print("Something went wrong when loading the page")
            driver.quit()

    driver.quit()