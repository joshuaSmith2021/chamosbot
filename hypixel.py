import json
import re
import requests

from utils import matrix

hypixel_api = json.loads(open('hypixel-api.json').read())

class PlayerCompare():
    def bedwars(self):
        table = matrix.Table(just='right')

        datasets = list(map(lambda x: x['player']['stats']['Bedwars'], self.datas))

        # Deaths must always be after kills, and final deaths after final kills!!!
        # Stats that are turned into ratios should have the numerator stat one index
        #   before the denominator stat. For example, KDR is kills/deaths, so deaths
        #   should come after kills.
        ratios = {'Deaths': 'KDR', 'Final Deaths': 'Final KDR', 'Games Played': 'Win %'}
        stats  = [
                    {
                        'key_name': 'eight_one_wins_bedwars',
                        'display': 'Solo Wins'
                    }, {
                        'key_name': 'eight_two_wins_bedwars',
                        'display': 'Duos Wins'
                    }, {
                        'key_name': 'four_four_wins_bedwars',
                        'display': 'Trios Wins'
                    }, {
                        'key_name': 'four_three_wins_bedwars',
                        'display': 'Quads Wins'
                    }, {
                        'key_name': 'wins_bedwars',
                        'display': 'Total Wins'
                    }, {
                        'key_name': 'games_played_bedwars',
                        'display': 'Games Played'
                    }, {
                        'key_name': 'kills_bedwars',
                        'display': 'Kills'
                    }, {
                        'key_name': 'deaths_bedwars',
                        'display': 'Deaths'
                    }, {
                        'key_name': 'final_kills_bedwars',
                        'display': 'Final Kills'
                    }, {
                        'key_name': 'final_deaths_bedwars',
                        'display': 'Final Deaths'
                    }
                ]

        # Construct basic table, but make every entry a string
        table.append(list(map(str, [''] + self.igns)))
        for stat in stats:
            table.append([stat['display']] + list(map(lambda x: str(x[stat['key_name']]), datasets)))# datasets[0][stat['key_name']], datasets[1][stat['key_name']]])

        # Replace death stats with KDRs
        for i, row in enumerate(table):
            # title, p1, p2 = row
            title = row[0]
            if title in ratios.keys():
                new_row = [ratios[title]]
                for j, value in enumerate(row[1:]):
                    new_row.append(round(int(table[i - 1][j + 1]) / int(table[i][j + 1]) * 1000) / 1000)
                table.insert(i + 1, list(map(str, new_row)))

        # if more than one player is being requested...
        if len(self.igns) > 1:
            # Highlight stat leaders, but skip the first row because it is just usernames
            for i, row in enumerate(table[1:]):
                best = min(map(float, row[1:])) if row[0] in ['Deaths', 'Final Deaths'] else max(map(float, row[1:]))
                best = re.sub(r'.0$', '', str(best))
                table[i + 1] = ['!!! ' + best if cell == best else cell for cell in row]# ['★★★ ' + best if cell == best else cell for cell in row]

        return table

    def __init__(self, igns):
        self.igns  = igns
        self.datas = []
        for ign in igns:
            self.datas.append(requests.get('https://api.hypixel.net/player?key={0}&name={1}'.format(hypixel_api['api-key'], ign)).json())


if __name__ == '__main__':
    playercomp = PlayerCompare(['parcerx', 'GL4CIER_FIST', 'ronansfire', 'Red_Lightning9', 'Catwing37'])
    result = (playercomp.bedwars())

    print(result)

    exit()
