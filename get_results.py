from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options as EdgeOptions
from time import sleep
import csv
import pandas as pd

def main(date=None):
    if not date:
        date = input("Date: ")
    options = EdgeOptions()
    options.add_argument('--start-maximized')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Edge(options=options)

    url = f'https://fantasy.espn.com/baseball/leaders?statSplit=singleScoringPeriod&scoringPeriodId=184'

    driver.get(url)
    sleep(2)

    text = '/td[2]/div'
    player_table = driver.find_element(By.XPATH, '//*[@id="fitt-analytics"]/div/div[5]/div[2]/div[3]/div/div/div/div/div/div/table[1]/tbody')
    sleep(1)
    stat_table = driver.find_element(By.XPATH, '//*[@id="fitt-analytics"]/div/div[5]/div[2]/div[3]/div/div/div/div/div/div/div/div[2]/table/tbody')
    sleep(1)
    player_rows = player_table.find_elements(By.TAG_NAME, 'tr')
    stat_rows = stat_table.find_elements(By.TAG_NAME, 'tr')
    length = len(player_rows)

    player_map = {}

    for i in range(length):
        # name
        player_tds = player_rows[i].find_elements(By.TAG_NAME, 'td')
        full_name = player_tds[0].find_element(By.TAG_NAME, 'div').get_attribute('title')
        name = full_name.split()[-1]
        if name == 'Jr.':
            name = ' '.join(name.split()[-2:])
        stat_tds = stat_rows[i].find_elements(By.TAG_NAME, 'td')
        bases = int(stat_tds[1].find_element(By.TAG_NAME, 'div').text)
        player_map[name] = bases

    '''
    WRITE
    '''
    # filename = 'test_file.csv'
    filename = f'{date}.csv'
    df = pd.read_csv(filename)
    print(player_map)
    df['Bases'] = df.apply(lambda x: player_map.get(x['Player']), axis=1)
    df.to_csv(filename)

    driver.quit()

if __name__ == '__main__':
    # 183
    main("2023-09-29")
    # main()