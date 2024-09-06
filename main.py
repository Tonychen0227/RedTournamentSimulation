from models.player import Player


### ELO RANGES
# High tier - 2000 - 1800
# Mid tier - 1800 - 1700
# Bottom tier - 1700 - 1500
from models.tournament import Tournament

players = [
    Player("Top High", 2000),
    Player("Mid High", 1900),
    Player("Bot High / Top Mid", 1800),
    Player("Mid Mid", 1750),
    Player("Bot Mid / Top Bottom", 1700),
    Player("Mid Bottom", 1600),
    Player("Bottom Bottom", 1500)
]


def run_sim_and_report(player_1, player_2, player_3):
    contestants = [player_1, player_2, player_3]

    rates = []

    for x in contestants:
        rates.append(x.expected_score_against_many([k for k in contestants if k != x]))

    rates_sum = sum(rates)
    rates = [k / rates_sum for k in rates]

    print("MATCH PREDICTION")
    for x in range(0, len(contestants)):
        print(f"{contestants[x].name}, win chance {round(rates[x] * 100, 2)}%")
    print("")


run_sim_and_report(players[0], players[3], players[6])
run_sim_and_report(players[0], players[1], players[2])
run_sim_and_report(players[2], players[3], players[4])

tournament = Tournament(49)
