from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
import re


def create_file(table_head, table_body):

    title = driver.find_element(By.XPATH, "//*[@id='main-content']/article/h1").text
    year = "".join(re.findall('[\d]+', title))

    try:
        # File creation
        f = open(f'{year}_sport.txt', 'a')
        try:
            f.write(f'{title}\n\n')
            f.write(table_head.text + '\n')

            for row in table_body:
                f.write(re.sub('\\n', " ", row.text) + '\n')

        except:
            print("Something went wrong when writing to the file")

        finally:
            f.close()
            return year

    except:
        print("Something went wrong when opening the file")


def display_record(table_body, year):

    wins = []
    losses = []
    draws = []

    for row in table_body:
        match = re.search("\s[W|L|T]\s", row.text)
        if match:
            char = (match.group()).strip()
            if char == 'W':
                wins.append(char)
            elif char == 'L':
                losses.append(char)
            else:
                draws.append(char)

    w = len(wins)
    l = len(losses)
    d = len(draws)
    wpct = ((w + (d * .5)) / ((w + (d * .5)) + (l + (d * .5))))

    # display team win-loss record
    print('\n{:>25} {}\n'.format('Team Win-Loss Record', year))
    print('{:^10}{:^10}{:^10}{:>5}\n{:^10}{:^10}{:^10}{:6.3f}'.format(
        'Wins', 'Losses', 'Draws', 'Win%', w, l, d, wpct))

    return wpct

"""
Basic overview of selenium over BeautifulSoup for web scrapping.
"""

if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.get('https://fgcuathletics.com/sports/womens-soccer/stats?path=wsoc')
    assert "Page not found" not in driver.page_source
    wpct = {}
    year = ""

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
                EC.presence_of_element_located((By.XPATH, "//*[@id='DataTables_Table_4']/thead/tr"))
            )

            table_body = driver.find_elements(By.XPATH, "//*[@id='DataTables_Table_4']/tbody/tr")

            year = create_file(table_head, table_body)

            wpct[year] = display_record(table_body, year) #Win pct

        except:
            print("Something went wrong when loading the page")
            driver.quit()

    driver.quit()

    best_season = {year for year in wpct if wpct[year] == max(wpct.values())}
    print(f"\nThe team's best season was in {''.join(best_season)}")


