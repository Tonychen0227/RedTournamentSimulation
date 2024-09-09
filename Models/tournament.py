from .bracket import Bracket
from .player import Player
from .round import Round
import math

default_elo_ranges = (1500, 1700, 1800, 2000)


class Tournament:
    def __init__(
        self, num_players: int, elo_ranges: tuple[int] = default_elo_ranges, should_print: bool = True
    ) -> None:

        (
            self.bottom_tier_low_elo,
            self.mid_tier_low_elo,
            self.top_tier_low_elo,
            self.top_tier_high_elo,
        ) = elo_ranges
        self.high_tier_size = math.ceil(num_players / 3)
        self.mid_tier_size = math.ceil((num_players - self.high_tier_size) / 2)
        self.low_tier_size = num_players - self.high_tier_size - self.mid_tier_size

        self.should_print = should_print

        if self.should_print:
            print(
                f"Tier Sizes: High={self.high_tier_size}, Mid={self.mid_tier_size}, Low={self.low_tier_size}"
            )

        self.players: list[Player] = []
        self.current_round = Round(self.should_print)

        # Generate players evenly amongst elo tiers
        for tier_size, tier_top_elo, tier_bottom_elo, tier_name in zip(
            (self.high_tier_size, self.mid_tier_size, self.low_tier_size),
            (self.top_tier_high_elo, self.top_tier_low_elo, self.mid_tier_low_elo),
            (self.top_tier_low_elo, self.mid_tier_low_elo, self.bottom_tier_low_elo),
            ("High", "Mid", "Low"),
        ):
            increment = (tier_top_elo - tier_bottom_elo) / (tier_size - 1)

            if self.should_print:
                print(f"low={tier_bottom_elo}, increment={increment}")

            for i in range(tier_size):
                name = f"{tier_name}_{i}"
                self.players.append(Player(name, tier_bottom_elo + (i * increment), self.should_print))

        for x in self.players:
            if self.should_print:
                print(f"Name: {x.name}, Rating: {round(x.rating, 2)}")

        for player in self.players:
            bracket = player.name.split("_")[0].upper()
            self.current_round.add_player(player, Bracket[bracket])

    def give_passive_points(self):
        self.current_round.give_passive_points()

    def run_round(self):
        results = self.current_round.generate_matches_and_simulate_round()
        next_round = Round(self.should_print)

        # Where you progress based on if you win or lose
        progressions = {
            Bracket.HIGH: [Bracket.HIGH, Bracket.MID],
            Bracket.MID: [Bracket.HIGH, Bracket.LOW],
            Bracket.LOW: [Bracket.MID, Bracket.LOW]
        }

        points_per_win = 4

        for bracket in results.keys():
            for result in results[bracket]:
                if self.should_print:
                    print(f"Processing result {result} from {bracket}")
                winner = result[0]
                loser = result[-1]

                winner.give_points(points_per_win)

                next_round.add_player(winner, progressions[bracket][0])
                next_round.add_player(loser, progressions[bracket][1])

                result.remove(winner)
                result.remove(loser)

                if len(result) > 0:
                    next_round.add_player(result[0], bracket)

        self.current_round = next_round

    def get_top_cut(self) -> list[Player]:
        sorted_by_second = sorted(self.players, key=lambda player: player.points, reverse=True)

        top_cut = []

        num_seen = 0
        last_seen_points = 0
        for player in sorted_by_second:
            if num_seen < 9:
                top_cut.append(player)
                num_seen += 1
                last_seen_points = player.points
            else:
                if player.points == last_seen_points:
                    top_cut.append(player)

        return (last_seen_points, top_cut)
