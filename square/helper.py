from square.player import Player
import random


def get_player_winrates(player_1: Player, player_2: Player, player_3: Player):
    contestants = [player_1, player_2, player_3]

    rates = []

    for x in contestants:
        rates.append(x.expected_score_against_many([k for k in contestants if k != x]))

    rates_sum = sum(rates)
    rates = [k / rates_sum for k in rates]

    ret = {}

    for i in range(0, 3):
        ret[contestants[i]] = rates[i]

    return ret


def simulate_match(players: list[Player]):
    results = []

    if len(players) == 3:
        win_rates = get_player_winrates(players[0], players[1], players[2])
        roll = random.random()

        winner = None
        cumulative = 0
        for x in win_rates.keys():
            cumulative += win_rates[x]
            if roll < cumulative:
                winner = x
                break

        results.append(winner)
        players.remove(winner)

    expected_points = players[0].expected_score_against(players[1])
    roll = random.random()
    if roll < expected_points:
        results.append(players[0])
        results.append(players[1])
    else:
        results.append(players[1])
        results.append(players[0])

    return results
