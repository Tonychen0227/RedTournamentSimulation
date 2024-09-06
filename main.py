from models.player import Player
from models.tournament import Tournament


def generate_players(mean_elo: int, range_sizes: list[int]) -> list[Player]:
    players = []
    players.append(Player("Top High", mean_elo + range_sizes[1]/2 + range_sizes[0]))
    players.append(Player("Mid High", mean_elo + range_sizes[1]/2 + range_sizes[0]/2))
    players.append(Player("Bot High / Top Mid", mean_elo + range_sizes[1]/2))
    players.append(Player("Mid Mid", mean_elo))
    players.append(Player("Bot Mid / Top Bottom", mean_elo - range_sizes[1]/2))
    players.append(Player("Mid Bottom", mean_elo - range_sizes[1]/2 - range_sizes[2]/2))
    players.append(Player("Bottom Bottom", mean_elo - range_sizes[1]/2 - range_sizes[2]))

    return players

def elo_ranges(mean_elo: int, range_sizes: list[int]) -> list[str]:
    ret = []
    ret.append(f"High Tier: {mean_elo + range_sizes[1]/2} - {mean_elo + range_sizes[1]/2 + range_sizes[0]}")
    ret.append(f"Mid Tier: {mean_elo - range_sizes[1]/2} - {mean_elo + range_sizes[1]/2}")
    ret.append(f"Bottom Tier: {mean_elo - range_sizes[1]/2 - range_sizes[2]} - {mean_elo - range_sizes[1]/2}")

    return ret

def run_sim_and_report(player_1: Player, player_2: Player, player_3: Player):
    contestants = [player_1, player_2, player_3]

    rates = []

    for x in contestants:
        rates.append(x.expected_score_against_many([k for k in contestants if k != x]))

    rates_sum = sum(rates)
    rates = [k / rates_sum for k in rates]

    print("MATCH PREDICTION")
    for x in range(0, len(contestants)):
        print(f"{contestants[x].name}, win chance {round(rates[x] * 100, 2)}%")
    print()


if __name__ == "__main__":
    mean_elo = 1400
    range_sizes = [300, 400, 800]
    players = generate_players(mean_elo, range_sizes)
    print("ELO Ranges:")
    for elo_range in elo_ranges(mean_elo, range_sizes):
        print(elo_range)

    print()
    run_sim_and_report(players[0], players[3], players[6])
    run_sim_and_report(players[0], players[1], players[2])
    run_sim_and_report(players[2], players[3], players[4])
    tournament = Tournament(49)
