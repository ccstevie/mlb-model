from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
import csv

def main():
    pitcher = input('Pitcher: ')
    batter = input('Batter: ')

    url = 'https://baseballsavant.mlb.com/'
    driver = webdriver.Edge()
    
    driver.get(url)
    sleep(5)
    element = driver.find_element(By.XPATH, '//*[@id="player-auto-complete"]')

    '''
    Pitcher
    '''

    element.send_keys(pitcher)
    sleep(5)
    element.send_keys(Keys.ENTER)
    sleep(5)

    pitcherStats = [pitcher]

    barrel = driver.find_element(By.XPATH, '//*[@id="text_percent_rank_barrel_batted_rate"]').text
    hardHit = driver.find_element(By.XPATH, '//*[@id="text_percent_rank_hard_hit_percent"]').text
    exitVelocity = driver.find_element(By.XPATH, '//*[@id="text_percent_rank_exit_velocity_avg"]').text
    pitcherStats.extend([barrel, hardHit, exitVelocity])

    '''
    BATTER
    '''

    element = driver.find_element(By.XPATH, '//*[@id="player-auto-complete"]')
    element.send_keys(batter)
    sleep(5)
    element.send_keys(Keys.ENTER)
    sleep(5)

    batterStats = [batter]

    barrel = driver.find_element(By.XPATH, '//*[@id="text_percent_rank_barrel_batted_rate"]').text
    hardHit = driver.find_element(By.XPATH, '//*[@id="text_percent_rank_hard_hit_percent"]').text
    exitVelocity = driver.find_element(By.XPATH, '//*[@id="text_percent_rank_exit_velocity_avg"]').text
    batterStats.extend([barrel, hardHit, exitVelocity])

    '''
    WRITE
    '''

    fields = ['Player', 'Barrel %', 'Hard Hit %', 'Average Exit Velocity']
    filename = f'{pitcher}-{batter}.csv'
    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        csvwriter.writerow(pitcherStats)
        csvwriter.writerow(batterStats)

    driver.quit()

if __name__ == '__main__':
    main()