import json
import re
import requests

from utils import matrix

hypixel_api = json.loads(open('credentials.json').read())['hypixel-api-key']

class PlayerCompare():
    def __build_table(self, datasets, stats, ratios=None):
        table = matrix.Table(just='right')

        # Construct basic table, but make every entry a string
        table.append(list(map(str, [''] + self.igns)))
        for stat in stats:
            table.append([stat['display']] + list(map(lambda x: str(x.get(stat['key_name'], 0)), datasets)))

        # Replace death stats with KDRs
        for i, row in enumerate(table):
            # title, p1, p2 = row
            title = row[0]
            if title in ratios.keys():
                new_row = [ratios[title]]
                for j, value in enumerate(row[1:]):
                    new_row.append(round(int(table[i - 1][j + 1]) / int(table[i][j + 1]) * 1000) / 1000)
                table.insert(i + 1, list(map(str, new_row)))

        return table

    def __highlight_winners(self, table, specials):
        # table is a matrix.Table, specials is a list of stats
        #   where the lower number is better, ie deaths
        for i, row in enumerate(table[1:]):
            best = min(map(float, row[1:])) if row[0] in specials else max(map(float, row[1:]))
            best = re.sub(r'.0$', '', str(best))
            table[i + 1] = ['!!! ' + best if cell == best else cell for cell in row]

        return table

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
                        'display': '4v4v4v4 Wins'
                    }, {
                        'key_name': 'two_four_wins_bedwars',
                        'display': '4v4 Wins'
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

        table = self.__build_table(datasets, stats, ratios=ratios)

        return table if len(self.igns) == 1 else self.__highlight_winners(table, ['Deaths', 'Final Deaths'])

    def skywars(self):
        table = matrix.Table(just='right')

        datasets = list(map(lambda x: x['player']['stats']['SkyWars'], self.datas))

        # Deaths must always be after kills, and final deaths after final kills!!!
        # Stats that are turned into ratios should have the numerator stat one index
        #   before the denominator stat. For example, KDR is kills/deaths, so deaths
        #   should come after kills.
        ratios = {'Total Deaths': 'KDR', 'Games Played': 'Win %'}
        stats  = [
                    {
                        'key_name': 'wins_solo',
                        'display': 'Solo Wins'
                    }, {
                        'key_name': 'wins_team',
                        'display': 'Team Wins'
                    }, {
                        'key_name': 'wins_mega',
                        'display': 'Mega Wins'
                    }, {
                        'key_name': 'wins_ranked',
                        'display': 'Ranked Wins'
                    }, {
                        'key_name': 'wins',
                        'display': 'Total Wins'
                    }, {
                        'key_name': 'games',
                        'display': 'Games Played'
                    }, {
                        'key_name': 'kills',
                        'display': 'Total Kills'
                    }, {
                        'key_name': 'deaths',
                        'display': 'Total Deaths'
                    }
                ]

        table = self.__build_table(datasets, stats, ratios=ratios)

        return table if len(self.igns) == 1 else self.__highlight_winners(table, ['Total Deaths'])


    def __init__(self, igns):
        self.igns  = igns
        self.datas = []
        for ign in igns:
            self.datas.append(requests.get('https://api.hypixel.net/player?key={0}&name={1}'.format(hypixel_api, ign)).json())

        # Validate data, and delete any datasets that had an invalid username
        bad_data = []
        for i, dataset in enumerate(self.datas):
            if dataset['success'] is False:
                bad_data.append(self.igns[i])
            elif dataset['player'] is None:
                bad_data.append(self.igns[i])

        for bad_name in bad_data:
            bad_index = self.igns.index(bad_name)
            del self.igns[bad_index]
            del self.datas[bad_index]


if __name__ == '__main__':
    playercomp = PlayerCompare(['parcerx', 'GL4CIER_FIST', 'ronansfire', 'Red_Lightning9', 'Catwing37'])
    #result = (playercomp.bedwars())

    print(playercomp.skywars())

    exit()
