from cleo import Command
import csv
import sys

class DetermineScoreCommand(Command):
    """
    Determine the scores of all the games

    determine:score
    """

    def handle(self):
        data_set = 'final_data.csv'
        output_set = 'scores.csv'

        columns = ['game_id', 'home_score', 'away_score']
        results = {}

        with open(data_set, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            i = 0
            for row in reader:
                if i > 0:
                    game_id = row[2]
                    if not game_id in results:
                        results[row[2]] = [0, 0]

                    if row[5] == "goal":
                        if self.is_home(row):
                            results[game_id][0] = results[game_id][0] + 1
                        else:
                            results[game_id][1] = results[game_id][1] + 1
                else:
                    i = i + 1

        with open(output_set, 'w+', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(columns)

            for game_id, goals in results.items():
                writer.writerow([game_id, goals[0], goals[1]])

    def is_home(self, row):
        if row[7] == row[22] or \
            row[7] == row[23] or \
            row[7] == row[24] or \
            row[7] == row[25] or \
            row[7] == row[26] or \
            row[7] == row[27]:
            return True
        else:
            return False
