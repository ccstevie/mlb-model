from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
import csv

def main():
    pitcher = input('Pitcher: ')
    team = input('Team (first letter capital): ')

    url = 'https://baseballsavant.mlb.com/'
    driver = webdriver.Edge()
    
    driver.get(url)
    driver.fullscreen_window()
    sleep(5)
    element = driver.find_element(By.XPATH, '//*[@id="player-auto-complete"]')

    '''
    Pitcher
    '''

    element.send_keys(pitcher)
    sleep(5)
    element.send_keys(Keys.ENTER)
    sleep(5)

    # barrel = driver.find_element(By.XPATH, '//*[@id="percentile-slider-viz"]/g/g[2]/g[2]/g[9]/g/text').text
    # hardHit = driver.find_element(By.XPATH, '//*[@id="text_percent_rank_hard_hit_percent"]').text
    # exitVelocity = driver.find_element(By.XPATH, '//*[@id="text_percent_rank_exit_velocity_avg"]').text
    # pitcherStats.extend([barrel, hardHit, exitVelocity])

    pitcherStats = {}
    container = driver.find_element(By.XPATH, '//*[@id="percentile-slider-viz"]').find_element(By.TAG_NAME, 'g').find_element(By.CLASS_NAME, 'pitching')
    pitchStats = container.find_element(By.CLASS_NAME, 'wrapper-pitching').find_elements(By.CLASS_NAME, 'metric')

    for stat in pitchStats:
        name = stat.find_element(By.TAG_NAME, 'text').text
        circle = stat.find_element(By.CLASS_NAME, 'circle-bulb')
        value = circle.find_element(By.TAG_NAME, 'text').text
        pitcherStats[name] = value

    '''
    TEAM
    '''

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
    filename = f'{pitcher}-{team}.csv'
    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        csvwriter.writerow(pitcherStats)
        csvwriter.writerows(teamStats)

    driver.quit()

if __name__ == '__main__':
    main()