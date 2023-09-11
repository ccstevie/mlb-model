from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv

def writeToCSV(name, data):
    # field names 
    fields = ['Team', 'Player', 'H', 'FF', 'FC', 'SI', 'CU', 'SL', 'KC', 'CH', 'FS']
        
    # name of csv file 
    filename = f'{name}.csv'

    # writing to csv file 
    with open(filename, 'w') as csvfile: 
        csvwriter = csv.writer(csvfile) 
        csvwriter.writerow(fields) 
        csvwriter.writerows(data)

def getPitcher(pitcher):
    url = 'https://ballparkpal.com/Pitcher-Research.php#'
    driver = webdriver.Edge()
    
    driver.get(url)
    time.sleep(5)

    driver.find_element(By.XPATH, '//*[@id="batters_table_filter"]/label/input').send_keys(pitcher)
    time.sleep(5)

    driver.find_element(By.XPATH, '//*[@id="batters_table_wrapper"]/div[2]/div/button[2]').click()
    time.sleep(5)

    parent = driver.find_element(By.XPATH, '//*[@id="batters_table"]/tbody/tr')
    children = parent.find_elements(By.XPATH, '*')

    pitcherStats = []

    for child in children:
        pitcherStats.append(child.text)

    driver.quit()

    return pitcherStats

def getBatter(batter):
    url = 'https://ballparkpal.com/Batter-Research.php#'
    driver = webdriver.Edge()
    
    driver.get(url)
    time.sleep(5)

    driver.find_element(By.XPATH, '//*[@id="batters_table_filter"]/label/input').send_keys(batter)
    time.sleep(5)

    driver.find_element(By.XPATH, '//*[@id="batters_table_wrapper"]/div[2]/div/button[2]').click()
    time.sleep(5)

    parent = driver.find_element(By.XPATH, '//*[@id="batters_table"]/tbody/tr')
    children = parent.find_elements(By.XPATH, '*')

    batterStats = []

    for child in children:
        batterStats.append(child.text)

    driver.quit()

    return batterStats

def main():
    pitcher = input('Pitcher: ')
    batter = input('Batter: ')
    rows = []
    rows.append(getPitcher(pitcher))
    rows.append(getBatter(batter))

    writeToCSV(f'{pitcher}-{batter}', rows)

if __name__ == '__main__':
    main()