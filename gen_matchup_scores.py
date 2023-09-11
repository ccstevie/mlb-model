from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options as EdgeOptions
from datetime import date
import csv

from gen_pitcher_stats import ballParkPal as getPitcherStats
from gen_batter_stats import ballParkPal as getAllBattersOfTeam
# import gen_team_stats

def getGames():
    url = 'https://www.rotowire.com/baseball/daily-lineups.php'
    options = EdgeOptions()
    options.add_argument('--start-maximized')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Edge(options=options)
    
    driver.get(url)
    
    # return values
    awayTeamAbbr, homeTeamAbbr, awayTeams, homeTeams, awayPitchers, homePitchers = ([] for i in range(6))

    path = '/html/body/div[1]/div/main/div[3]'
    lineups = driver.find_element(By.CLASS_NAME, 'lineups').find_elements(By.CLASS_NAME, 'lineup')
    for index, lineup in enumerate(lineups[:-2]):
        if index == 4:
            continue
        abbrA = lineup.find_element(By.XPATH, f'{path}/div[{index+1}]/div[2]/div[1]/div/div[1]/div').text
        abbrH = lineup.find_element(By.XPATH, f'{path}/div[{index+1}]/div[2]/div[1]/div/div[2]/div').text
        if abbrA == 'CWS':
            abbrA = 'CHW'
        if abbrH == 'CWS':
            abbrH = 'CHW'
        awayTeamAbbr.append(abbrA)
        homeTeamAbbr.append(abbrH)
        nameArray = lineup.find_element(By.XPATH, f'{path}/div[{index+1}]/div[2]/a/div[1]').text.split()
        if len(nameArray) > 2:
            awayTeams.append(' '.join(nameArray[0:2]))
        else:
            awayTeams.append(lineup.find_element(By.XPATH, f'{path}/div[{index+1}]/div[2]/a/div[1]').text.split()[0])
        homeTeams.append(lineup.find_element(By.XPATH, f'{path}/div[{index+1}]/div[2]/a/div[2]').text.split()[0])
        awayPitchers.append(lineup.find_element(By.XPATH, f'{path}/div[{index+1}]/div[2]/div[2]/ul[1]/li[1]/div[1]/a').text.split()[1])
        homePitchers.append(lineup.find_element(By.XPATH, f'{path}/div[{index+1}]/div[2]/div[2]/ul[2]/li[1]/div[1]/a').text.split()[1])

    driver.quit()

    return awayTeamAbbr, homeTeamAbbr, awayTeams, homeTeams, awayPitchers, homePitchers

def main():
    awayTeamAbbr, homeTeamAbbr, awayTeams, homeTeams, awayPitchers, homePitchers = getGames()

    # for awayTeam in awayTeams:
    #     gen_team_stats.main(awayTeam)

    # for homeTeam in homeTeams:
    #     gen_team_stats.main(homeTeam)

    batterMap = {}
    batListA, batListH, pitchListA, pitchListH = ([] for i in range(4))

    for name in awayTeamAbbr:
        awayBatterStats = getAllBattersOfTeam(name)
        batListA.append(awayBatterStats)

    for name in homeTeamAbbr:
        homeBatterStats = getAllBattersOfTeam(name)
        if name == 'KC':
            homeBatterStats = homeBatterStats[1:]
        batListH.append(homeBatterStats)

    for index, awayPitcher in enumerate(awayPitchers):
        awayPT, awayPP, awayPO, awayLines, awayHand = getPitcherStats(awayPitcher, awayTeamAbbr[index])
        pitchListA.append([awayPT, awayPP, awayPO, awayLines, awayHand])

    for index, homePitcher in enumerate(homePitchers):
        homePT, homePP, homePO, homeLines, homeHand = getPitcherStats(homePitcher, homeTeamAbbr[index])
        pitchListH.append([homePT, homePP, homePO, homeLines, homeHand])

    numGames = len(pitchListH)

    for i in range(numGames):
        if not pitchListH[i][0]:
            continue
        for player in batListA[i]:
            score = 0
            for j in range(3, 11):
                if not pitchListH[i][0][j]:
                   continue 
                weight = (float(player[j]) - float(pitchListH[i][0][j])) * float(pitchListH[i][1][j])
                score += weight
            cmp = (float(player[11]) + float(pitchListH[i][2][0]))/2 - 0.051
            xbh = (cmp*100/0.051) * (100/125)
            score += xbh
            cmp = (float(player[12]) + float(pitchListH[i][2][1]))/2 - 0.23
            bb = (cmp*100/0.23) * (100/125)
            score += bb
            cmp = (float(player[13]) + float(pitchListH[i][2][2]))/2 - 0.103
            so = (cmp*100/0.103) * (100/125)
            score += so
            cmp = (float(player[14]) + float(pitchListH[i][3][0]))/2 - 0.227
            line = (cmp*100/0.227) * (100/125)
            score += line
            diff = 0
            if (player[2] == "L"):
                if (pitchListH[i][0][2] == "L"):
                    diff = (float(player[15]) - float(pitchListH[i][4][0]))
                else:
                    diff = (float(player[16]) - float(pitchListH[i][4][0]))
            else:
                if (pitchListH[i][0][2] == "L"):
                    diff = (float(player[15]) - float(pitchListH[i][4][1]))
                else:
                    diff = (float(player[16]) - float(pitchListH[i][4][1]))
            score += diff
            if len(player) > 17:
                opsFactor = float(player[17]) - .736 + 1
                score *= opsFactor

            batterMap[player[1]] = round(score, 1)

    for i in range(numGames):
        if len(pitchListA[i][0]) < 2:
            continue
        for player in batListH[i]:
            score = 0
            for j in range(3, 11):
                if not pitchListA[i][0][j]:
                   continue 
                weight = (float(player[j]) - float(pitchListA[i][0][j])) * float(pitchListA[i][1][j])
                score += weight
            cmp = (float(player[11]) + float(pitchListA[i][2][0]))/2 - 0.051
            xbh = (cmp*100/0.051) * (100/125)
            score += xbh
            cmp = (float(player[12]) + float(pitchListA[i][2][1]))/2 - 0.23
            bb = (cmp*100/0.23) * (100/125)
            score += bb
            cmp = (float(player[13]) + float(pitchListA[i][2][2]))/2 - 0.103
            so = (cmp*100/0.103) * (100/125)
            score += so
            cmp = (float(player[14]) + float(pitchListA[i][3][0]))/2 - 0.227
            line = (cmp*100/0.227) * (100/125)
            score += line
            diff = 0
            if (player[2] == "L"):
                if (pitchListA[i][0][2] == "L"):
                    diff = (float(player[15]) - float(pitchListA[i][4][0]))
                else:
                    diff = (float(player[16]) - float(pitchListA[i][4][0]))
            else:
                if (pitchListA[i][0][2] == "L"):
                    diff = (float(player[15]) - float(pitchListA[i][4][1]))
                else:
                    diff = (float(player[16]) - float(pitchListA[i][4][1]))
            score += diff
            if len(player) > 17:
                opsFactor = float(player[17]) - .736 + 1
                score *= opsFactor
            batterMap[player[1]] = round(score)

    sorterBatterMap = {k: v for k, v in sorted(batterMap.items(), key=lambda item: item[1], reverse=True)}

    with open(f'{date.today()}.csv','w', newline='') as f:
        w = csv.writer(f)
        w.writerows(sorterBatterMap.items())

if __name__ == '__main__':
    main()