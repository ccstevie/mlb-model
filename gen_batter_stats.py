from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.edge.options import Options as EdgeOptions
from time import sleep
import re

def ballParkPal(team):
    print(team)
    options = EdgeOptions()
    # options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Edge(options=options)
    driver.implicitly_wait(10)
    
    driver.get("https://ballparkpal.com/ParkFactors.php")

    table = driver.find_element(By.XPATH, '/html/body/div[1]/table/tbody/tr')
    row = table.find_element(By.XPATH, f'//*[contains(text(), "{team}")]')
    tr = row.find_element(By.XPATH, '../../..')
    td = tr.find_elements(By.TAG_NAME, 'td')
    parkFactor = 1 + (float(re.sub(r"[^0-9.]", "", td[4].text))/100)
    
    url = 'https://ballparkpal.com/Batter-Research.php#'
    driver.get(url)

    driver.find_element(By.XPATH, '//*[@id="batters_table_wrapper"]/div[2]/div/button[2]').click()
    sleep(1)

    parent = driver.find_element(By.XPATH, '//*[@id="batters_table"]/tbody/tr')
    children = parent.find_elements(By.XPATH, f'//*[contains(text(), "{team}")]')

    batterStats = []

    for child in children:
        body = child.find_element(By.XPATH, '..')
        batterData = body.find_elements(By.TAG_NAME, 'td')
        rowData = []
        for data in batterData:
            rowData.append(data.text)
        if len(rowData) > 0:
            batterStats.append(rowData)

    driver.find_element(By.XPATH, '//*[@id="batters_table_wrapper"]/div[2]/div/button[6]').click()
    sleep(1)

    parent = driver.find_element(By.XPATH, '//*[@id="batters_table"]/tbody/tr')
    children = parent.find_elements(By.XPATH, f'//*[contains(text(), "{team}")]')

    for index, child in enumerate(children):
        body = child.find_element(By.XPATH, '..')
        batterData = body.find_elements(By.TAG_NAME, 'td')
        batterStats[index].extend([batterData[5].text, batterData[7].text, batterData[8].text])

    driver.find_element(By.XPATH, '//*[@id="batters_table_wrapper"]/div[2]/div/button[7]').click()
    sleep(1)

    parent = driver.find_element(By.XPATH, '//*[@id="batters_table"]/tbody/tr')
    children = parent.find_elements(By.XPATH, f'//*[contains(text(), "{team}")]')

    for index, child in enumerate(children):
        body = child.find_element(By.XPATH, '..')
        batterData = body.find_elements(By.TAG_NAME, 'td')
        batterStats[index].extend([batterData[4].text])

    driver.find_element(By.XPATH, '//*[@id="batters_table_wrapper"]/div[2]/div/button[1]').click()
    sleep(1)

    parent = driver.find_element(By.XPATH, '//*[@id="batters_table"]/tbody/tr')
    children = parent.find_elements(By.XPATH, f'//*[contains(text(), "{team}")]')

    for index, child in enumerate(children):
        body = child.find_element(By.XPATH, '..')
        batterData = body.find_elements(By.TAG_NAME, 'td')
        batterStats[index].extend([batterData[3].text, batterData[4].text])
    
    driver.get('https://www.fantasypros.com/mlb/stats/hitters.php?range=7&page=ALL')

    # find table
    table = driver.find_element(By.CLASS_NAME, 'mobile-table')
    sleep(1)

    if team == 'CHW':
        team = 'CWS'

    for index, batter in enumerate(batterStats):
        try:
            lastName = batter[1].split(' ')[1]
            element = table.find_elements(By.XPATH, f'//*[contains(text(), "{lastName}")]')

            for player in element:
                td = player.find_element(By.XPATH, '..')
                playerTeam = td.find_element(By.XPATH, './/small/a').text
                if playerTeam == team:
                    row = td.find_element(By.XPATH, '..')
                    ops = row.find_elements(By.TAG_NAME, 'td')[15].text
                    batterStats[index].append(ops)

        except NoSuchElementException:
            continue

    return batterStats, parkFactor

def main():
    print(ballParkPal('HOU'))

if __name__ == '__main__':
    main()