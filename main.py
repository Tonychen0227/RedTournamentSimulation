import statistics

from models.helpers import Helpers
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
    rates = Helpers.get_player_winrates(player_1, player_2, player_3)

    print("MATCH PREDICTION")
    for x in rates.keys():
        print(f"{x.name}, win chance {round(rates[x] * 100, 2)}%")
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

    top_cut_summary = {}
    cutoff = []
    size_of_cut = {}

    num_trials = 10000

    for i in range(0, num_trials):
        tournament = Tournament(49, generate_elo_ranges, False)

        for x in range(1, 4):
            tournament.give_passive_points()
            tournament.run_round()

        tournament_top_cut = tournament.get_top_cut()

        top_cut = tournament_top_cut[1]
        top_cut_cutoff = tournament_top_cut[0]

        cutoff.append(top_cut_cutoff)

        size_of_topcut = len(top_cut)
        if size_of_topcut not in size_of_cut:
            size_of_cut[size_of_topcut] = 0

        size_of_cut[size_of_topcut] += 1

        for x in top_cut:
            if x.name not in top_cut_summary:
                top_cut_summary[x.name] = 0

            top_cut_summary[x.name] += 1

    print(statistics.mean(cutoff))
    print(f"Size of top cut: average={statistics.mean(size_of_cut)}, max={max(size_of_cut)}, min={min(size_of_cut)}")

    top_cut_summary = {k: f"Cut rate {round((v / num_trials) * 100, 2)}%" for k, v in sorted(top_cut_summary.items(), key=lambda item: item[1], reverse=True)}
    print(top_cut_summary)

    top_cut_counts = {k: f"Rate {round((v / num_trials) * 100, 2)}%" for k, v in
                       sorted(size_of_cut.items(), key=lambda item: item[1], reverse=True)}
    print(top_cut_counts)