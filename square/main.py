import statistics
import json
import jsonpickle

from square.enums import PlayoffOrder, Bracket
from square.tournament import Tournament

if __name__ == "__main__":
    top_cut_summary = {}
    cutoff = []
    size_of_cut = {}

    num_trials = 10000

    for i in range(0, num_trials):
        tournament = Tournament(num_players=54)

        tournament.assign_matches()
        tournament.run_matches(0, 0, 10, 9, 6, PlayoffOrder.NONE)

        tournament.assign_matches()
        tournament.run_matches(10, 6, 10, 6, 3, PlayoffOrder.FIRST)

        tournament.assign_matches()
        tournament.run_matches(10, 6, 10, 6, 3, PlayoffOrder.SECOND)

        tournament_top_cut = tournament.get_top_cut()

        top_cut = tournament_top_cut[0]
        top_cut_cutoff = tournament_top_cut[1]

        cutoff.append(top_cut_cutoff)

        size_of_topcut = len(top_cut)
        if size_of_topcut not in size_of_cut:
            size_of_cut[size_of_topcut] = 0

        size_of_cut[size_of_topcut] += 1

        for x in top_cut:
            if x.name not in top_cut_summary:
                top_cut_summary[x.name] = 0

            top_cut_summary[x.name] += 1

    print(f"Average cutoff: {statistics.mean(cutoff)}")
    print(f"Size of top cut: average={statistics.mean(size_of_cut)}, max={max(size_of_cut)}, min={min(size_of_cut)}")

    top_cut_summary = {k: f"Cut rate {round((v / num_trials) * 100, 2)}%" for k, v in sorted(top_cut_summary.items(), key=lambda item: item[1], reverse=True)}
    print(top_cut_summary)

    top_cut_counts = {k: f"Rate {round((v / num_trials) * 100, 2)}%" for k, v in
                       sorted(size_of_cut.items(), key=lambda item: item[1], reverse=True)}
    print(top_cut_counts)
