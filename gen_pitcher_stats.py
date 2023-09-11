from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options as EdgeOptions
from time import sleep
import csv

def ballParkPal(pitcher, team):
    options = EdgeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    url = 'https://ballparkpal.com/Pitcher-Research.php#'
    driver = webdriver.Edge(options=options)
    driver.implicitly_wait(10)
    
    driver.get(url)

    driver.find_element(By.XPATH, '//*[@id="batters_table_filter"]/label/input').send_keys(pitcher)
    sleep(1)

    driver.find_element(By.XPATH, '//*[@id="batters_table_wrapper"]/div[2]/div/button[2]').click()
    sleep(1)
    
    pitchType = []

    typeParent = driver.find_element(By.XPATH, '//*[@id="batters_table"]/tbody')
    typeChildren = typeParent.find_elements(By.TAG_NAME, 'tr')

    if len(typeChildren) > 1:
        correctPlayer = typeParent.find_element(By.XPATH, f'//*[contains(text(), "{team}")]')
        tr = correctPlayer.find_element(By.XPATH, '..')
        row = tr.find_elements(By.XPATH, '*')
        if row[0].text == "No matching records found":
            return [], [], [], [], []
        for data in row:
            pitchType.append(data.text)
    else:
        row = typeChildren[0].find_elements(By.XPATH, '*')
        if row[0].text == "No matching records found":
            return [], [], [], [], []
        for data in row:
            pitchType.append(data.text)

    driver.find_element(By.XPATH, '//*[@id="batters_table_wrapper"]/div[2]/div/button[3]').click()
    sleep(1)

    pitchPct = []

    pctParent = driver.find_element(By.XPATH, '//*[@id="batters_table"]/tbody')
    pctChildren = pctParent.find_elements(By.TAG_NAME, 'tr')

    if len(pctChildren) > 1:
        correctPlayer = pctParent.find_element(By.XPATH, f'//*[contains(text(), "{team}")]')
        tr = correctPlayer.find_element(By.XPATH, '..')
        row = tr.find_elements(By.XPATH, '*')
        for data in row:
            pitchPct.append(data.text)
    else:
        row = pctChildren[0].find_elements(By.XPATH, '*')
        for data in row:
            pitchPct.append(data.text)

    driver.find_element(By.XPATH, '//*[@id="batters_table_wrapper"]/div[2]/div/button[7]').click()
    sleep(1)

    pitchOutcome = []

    outcomeParent = driver.find_element(By.XPATH, '//*[@id="batters_table"]/tbody')
    outcomeChildren = outcomeParent.find_elements(By.TAG_NAME, 'tr')

    if len(outcomeChildren) > 1:
        correctPlayer = pctParent.find_element(By.XPATH, f'//*[contains(text(), "{team}")]')
        tr = correctPlayer.find_element(By.XPATH, '..')
        row = tr.find_elements(By.XPATH, '*')
        pitchOutcome.extend([row[5].text, row[7].text, row[8].text])
    else:
        row = outcomeChildren[0].find_elements(By.XPATH, '*')
        pitchOutcome.extend([row[5].text, row[7].text, row[8].text])

    driver.find_element(By.XPATH, '//*[@id="batters_table_wrapper"]/div[2]/div/button[8]').click()
    sleep(1)

    line = []

    lineParent = driver.find_element(By.XPATH, '//*[@id="batters_table"]/tbody')
    lineChildren = lineParent.find_elements(By.TAG_NAME, 'tr')

    if len(lineChildren) > 1:
        correctPlayer = pctParent.find_element(By.XPATH, f'//*[contains(text(), "{team}")]')
        tr = correctPlayer.find_element(By.XPATH, '..')
        row = tr.find_elements(By.XPATH, '*')
        line.append(row[4].text)
    else:
        row = lineChildren[0].find_elements(By.XPATH, '*')
        line.append(row[4].text)

    driver.find_element(By.XPATH, '//*[@id="batters_table_wrapper"]/div[2]/div/button[1]').click()
    sleep(1)

    handedness = []

    handednessParent = driver.find_element(By.XPATH, '//*[@id="batters_table"]/tbody')
    handednessChildren = handednessParent.find_elements(By.TAG_NAME, 'tr')

    if len(handednessChildren) > 1:
        correctPlayer = pctParent.find_element(By.XPATH, f'//*[contains(text(), "{team}")]')
        tr = correctPlayer.find_element(By.XPATH, '..')
        row = tr.find_elements(By.XPATH, '*')
        handedness.extend([row[3].text, row[4].text])
    else:
        row = handednessChildren[0].find_elements(By.XPATH, '*')
        handedness.extend([row[3].text, row[4].text])

    return pitchType, pitchPct, pitchOutcome, line, handedness

def baseballSavant(pitcher):
    url = 'https://baseballsavant.mlb.com/'
    driver = webdriver.Edge()
    
    driver.get(url)
    driver.fullscreen_window()
    element = driver.find_element(By.XPATH, '//*[@id="player-auto-complete"]')

    element.send_keys(pitcher)
    element.send_keys(Keys.ENTER)

    # barrel = driver.find_element(By.XPATH, '//*[@id="percentile-slider-viz"]/g/g[2]/g[2]/g[9]/g/text').text
    # hardHit = driver.find_element(By.XPATH, '//*[@id="text_percent_rank_hard_hit_percent"]').text
    # exitVelocity = driver.find_element(By.XPATH, '//*[@id="text_percent_rank_exit_velocity_avg"]').text
    # pitcherStats.extend([barrel, hardHit, exitVelocity])

    pitchCats = []
    pitchVals = []
    container = driver.find_element(By.XPATH, '//*[@id="percentile-slider-viz"]').find_element(By.TAG_NAME, 'g').find_element(By.CLASS_NAME, 'pitching')
    pitchStats = container.find_element(By.CLASS_NAME, 'wrapper-pitching').find_elements(By.CLASS_NAME, 'metric')

    for stat in pitchStats:
        name = stat.find_element(By.TAG_NAME, 'text').text
        circle = stat.find_element(By.CLASS_NAME, 'circle-bulb')
        value = circle.find_element(By.TAG_NAME, 'text').text
        pitchCats.append(name)
        pitchVals.append(value)
    
    return pitchCats, pitchVals

def main(pitcher=None):
    if not pitcher:
        pitcher = input('Pitcher: ')

    filename = f'{pitcher}.csv'
    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)

        pitchTypes, pitchPcts, pitchOucomes, lines, handedness = ballParkPal(pitcher, 'LAD')
        # categories, values = baseballSavant(pitcher)

        csvwriter.writerow(['Team', 'Player', 'H', 'FF', 'FC', 'SI', 'CU', 'SL', 'KC', 'CH', 'FS'])
        csvwriter.writerow(pitchTypes)
        csvwriter.writerow(pitchPcts)
        csvwriter.writerow(pitchOucomes)
        csvwriter.writerow(lines)
        csvwriter.writerow(handedness)
        # csvwriter.writerow(categories)
        # csvwriter.writerow(values)

if __name__ == '__main__':
    main()