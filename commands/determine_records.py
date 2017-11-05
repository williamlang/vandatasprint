from cleo import Command
import csv
import sys

class DetermineRecordCommand(Command):
    """
    Determine the records for teams

    determine:record
    """

    def handle(self):
        data_set = 'final_data.csv'
        output_set = 'team_records.csv'

        columns = ['team_id', 'wins', 'losses', 'otl']
        results = {}
        teams = {}

        with open(data_set, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            i = 0
            for row in reader:
                if i > 0:
                    game_id = row[2]
                    if not game_id in results:
                        results[game_id] = {
                            'home_goals': 0,
                            'away_goals': 0,
                            'periods': 0,
                            'home_team': -1,
                            'away_team': -1
                        }

                    if row[5] == "goal":
                        if self.is_home(row):
                            results[game_id]['home_goals'] = results[game_id]['home_goals'] + 1
                        else:
                            results[game_id]['away_goals'] = results[game_id]['away_goals'] + 1

                    results[game_id]['periods'] = max(results[game_id]['periods'], int(row[4]))
                    results[game_id]['home_team'] = row[12]
                    results[game_id]['away_team'] = row[13]
                else:
                    i = i + 1

        with open(output_set, 'w+', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(columns)

            for game_id, game in results.items():
                home_team = game['home_team']
                away_team = game['away_team']

                if not home_team in teams:
                    teams[home_team] = [home_team, 0, 0, 0]

                if not away_team in teams:
                    teams[away_team] = [away_team, 0, 0, 0]

                if game['home_goals'] > game['away_goals']:
                    teams[home_team][1] = teams[home_team][1] + 1
                else:
                    teams[away_team][1] = teams[away_team][1] + 1

                if game['periods'] == 3:
                    if game['home_goals'] > game['away_goals']:
                        teams[away_team][2] = teams[away_team][2] + 1
                    else:
                        teams[home_team][2] = teams[home_team][2] + 1
                else:
                    if game['home_goals'] > game['away_goals']:
                        teams[away_team][3] = teams[away_team][3] + 1
                    else:
                        teams[home_team][3] = teams[home_team][3] + 1

            for team_id, record in teams.items():
                writer.writerow([team_id, record[1], record[2], record[3]])

    def is_home(self, row):
        if row[3] == row[12]:
            return True
        else:
            return False
