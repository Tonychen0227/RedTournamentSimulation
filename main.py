from models.player import Player
from models.tournament import Tournament
from typing import Iterable


def generate_elo_ranges(mean_elo: int, range_sizes: Iterable[int]) -> tuple[int]:
    return (
        mean_elo - range_sizes[1] / 2 - range_sizes[2],  # bottom of low
        mean_elo - range_sizes[1] / 2,  # top of low
        mean_elo + range_sizes[1] / 2,  # bottom of top
        mean_elo + range_sizes[1] / 2 + range_sizes[0],  # top of top
    )


def generate_players(mean_elo: int, range_sizes: list[int]) -> list[Player]:
    ranges = generate_elo_ranges(mean_elo, range_sizes)
    players = []
    players.append(Player("Top High", ranges[3]))
    players.append(Player("Mid High", (ranges[3] + ranges[2]) / 2))
    players.append(Player("Bot High / Top Mid", ranges[2]))
    players.append(Player("Mid Mid", mean_elo))
    players.append(Player("Bot Mid / Top Bottom", ranges[1]))
    players.append(Player("Mid Bottom", (ranges[1] + ranges[0]) / 2))
    players.append(Player("Bottom Bottom", ranges[0]))

    return players


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
    generate_elo_ranges = generate_elo_ranges(mean_elo, range_sizes)

    print("ELO Ranges:")
    print(f"Bottom Tier: {generate_elo_ranges[0]} - {generate_elo_ranges[1]}")
    print(f"Mid Tier: {generate_elo_ranges[1]} - {generate_elo_ranges[2]}")
    print(f"High Tier: {generate_elo_ranges[2]} - {generate_elo_ranges[3]}")

    print()
    run_sim_and_report(players[0], players[3], players[6])
    run_sim_and_report(players[0], players[1], players[2])
    run_sim_and_report(players[2], players[3], players[4])
    tournament = Tournament(49, generate_elo_ranges)
