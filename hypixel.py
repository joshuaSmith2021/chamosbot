import json
import re
import requests

from utils import matrix

hypixel_api = json.loads(open('credentials.json').read())['hypixel-api-key']

class PlayerCompare():
    def __build_table(self):
        datasets = self.datasets
        stats = self.stats
        ratios = self.ratios
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

        return table if len(self.igns) == 1 else self.__highlight_winners(table)

    def __highlight_winners(self, table):
        specials = self.reverse_stats
        # table is a matrix.Table, specials is a list of stats
        #   where the lower number is better, ie deaths
        for i, row in enumerate(table[1:]):
            best = min(map(float, row[1:])) if row[0] in specials else max(map(float, row[1:]))
            best = re.sub(r'.0$', '', str(best))
            table[i + 1] = ['!!! ' + best if cell == best else cell for cell in row]

        return table

    def __init__(self, igns):
        self.igns = igns
        self.datasets = []
        self.datas = []
        self.fails = []
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
            self.fails.append(bad_name)

        # Build datasets
        for i, data in enumerate(self.datas):
            dataset = data
            for key in self.keys:
                dataset = dataset[key]
            self.datasets.append(dataset)

    def __str__(self):
        table = self.__build_table()
        fail_string = ''
        if len(self.fails) > 0:
            fail_string = '\n\nNo data found for the following player{0}: {1}'.format('s' if len(self.fails) > 1 else '', ', '.join(self.fails))
            fail_string += '\nTry checking the spelling of the name'
        return '{0}{1}'.format(str(table), fail_string)


class Bedwars(PlayerCompare):
    keys = ['player', 'stats', 'Bedwars']
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
    reverse_stats = ['Deaths', 'Final Deaths']


class Skywars(PlayerCompare):
    keys = ['player', 'stats', 'SkyWars']
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

    reverse_stats = ['Deaths']


class Pit(PlayerCompare):
    keys = ['player', 'stats', 'Pit', 'pit_stats_ptl']
    ratios = [
                {
                    'display'  : 'KDR',
                    'calculate': 'kills / deaths',
                    'position': 'Deaths'
                }, {
                    'display'  : 'K+A DR',
                    'calculate': '(kills + assists) / deaths',
                    'position' : 'KDR'
                }
        ]

    stats = [
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

    reverse_stats = ['Deaths']


if __name__ == '__main__':
    # playercomp = PlayerCompare(['parcerx', 'GL4CIER_FIST', 'ronansfire', 'Red_Lightning9', 'Catwing37'])
    #result = (playercomp.bedwars())
    new = Bedwars(['parcerx', 'Red_Lightning9', 'Gl4CIER_FIST', 'ronansfire', 'Catwing37'])
    print(new)
    # print(playercomp.pit())

    exit()
