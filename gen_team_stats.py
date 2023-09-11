from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
import csv

def main(team=None):
    if not team:
        team = input('Team (first letter capital): ')

    url = 'https://baseballsavant.mlb.com/'
    driver = webdriver.Edge()
    
    driver.get(url)
    driver.fullscreen_window()
    sleep(5)

    element = driver.find_element(By.XPATH, '//*[@id="player-auto-complete"]')
    element.send_keys(team)
    sleep(5)
    element.send_keys(Keys.ENTER)
    sleep(5)

    table = driver.find_element(By.XPATH, '//*[@id="statcastHitting"]/div[2]/table')
    rows = table.find_elements(By.TAG_NAME, 'tr')
    teamStats = []

    for row in rows[2:]:
        playerStats = []
        tds = row.find_elements(By.TAG_NAME, 'td')
        playerStats.extend([tds[0].text, tds[18].text, tds[19].text, tds[20].text])
        teamStats.append(playerStats)

    '''
    WRITE
    '''

    fields = ['Player', 'Barrel %', 'Hard Hit %', 'Exit Velocity']
    filename = f'{team}.csv'
    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        csvwriter.writerows(teamStats)

    driver.quit()

if __name__ == '__main__':
    main()