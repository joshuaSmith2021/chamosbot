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


        if ratios is not None:
            for ratio in ratios:
                new_row = [ratio['display']]
                for dataset in datasets:
                    # Substitute in the actual values for calculation using re.sub
                    expression = re.sub(r'[^+\-*/\s\(\)]+', lambda x: str(dataset[x.group(0)]), ratio['calculate'])
                    # Use python eval and add the element to the list
                    new_row.append(str(round(eval(expression) * 1000) / 1000))

                # This bit is a little complicated, but I use zip(*table)[0] to get a list of the
                #   row titles, then I get the index of the correct row and add 1 to it in order
                #   to insert the new row in the desired position
                table.insert(list(zip(*table))[0].index(ratio['position']) + 1, new_row)
        # Replace death stats with KDRs
        #for i, row in enumerate(table):
        #    # title, p1, p2 = row
        #    title = row[0]
        #    if title in ratios.keys():
        #        new_row = [ratios[title]]
        #        for j, value in enumerate(row[1:]):
        #            new_row.append(round(int(table[i - 1][j + 1]) / int(table[i][j + 1]) * 1000) / 1000)
        #        table.insert(i + 1, list(map(str, new_row)))

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

        # ratios is a list of categories that are calculated from other values in the data.
        #   Each dictionary shoould have three attrivutes:
        #   - display, which represents the name of the row on the final table
        #   - calculate, a string representing how the value is calculated.
        #     This string is later put through Python's eval() function
        #   - position, the name of the row that the result should end up under.
        ratios = [
                    {
                        'display'  : 'KDR',
                        'calculate': 'kills_bedwars / deaths_bedwars',
                        'position' : 'Deaths'
                    }, {
                        'display'  : 'Win %',
                        'calculate': 'wins_bedwars / games_played_bedwars',
                        'position' : 'Games Played'
                    }, {
                        'display'  : 'Final KDR',
                        'calculate': 'final_kills_bedwars / final_deaths_bedwars',
                        'position' : 'Final Deaths'
                    }
            ]
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
        ratios = [
                    {
                        'display'  : 'KDR',
                        'calculate': 'kills / deaths',
                        'position' : 'Deaths'
                    }, {
                        'display'  : 'Win %',
                        'calculate': 'wins / games',
                        'position' : 'Games Played'
                    }
            ]
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
                        'display': 'Kills'
                    }, {
                        'key_name': 'deaths',
                        'display': 'Deaths'
                    }
                ]

        table = self.__build_table(datasets, stats, ratios=ratios)

        return table if len(self.igns) == 1 else self.__highlight_winners(table, ['Total Deaths'])

    def pit(self):
        table = matrix.Table(just='right')

        datasets = list(map(lambda x: x['player']['stats']['Pit']['pit_stats_ptl'], self.datas))

        # Deaths must always be after kills, and final deaths after final kills!!!
        # Stats that are turned into ratios should have the numerator stat one index
        #   before the denominator stat. For example, KDR is kills/deaths, so deaths
        #   should come after kills.
        ratios = [
                    {
                        'display': 'KDR',
                        'calculate': 'kills / deaths',
                        'position': 'Deaths'
                    }, {
                        'display': 'K+A DR',
                        'calculate': '(kills + assists) / deaths',
                        'position': 'KDR'
                    }
            ]
        stats  = [
                    {
                        'key_name': 'playtime_minutes',
                        'display': 'Minutes'
                    }, {
                        'key_name': 'kills',
                        'display': 'Kills'
                    }, {
                        'key_name': 'assists',
                        'display': 'Assists'
                    }, {
                        'key_name': 'deaths',
                        'display': 'Deaths'
                    }, {
                        'key_name': 'max_streak',
                        'display': 'Best Streak'
                    }
                ]

        table = self.__build_table(datasets, stats, ratios=ratios)

        return table if len(self.igns) == 1 else self.__highlight_winners(table, ['Deaths'])


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

    print(playercomp.pit())

    exit()
