from .bracket import Bracket
from .player import Player
from .round import Round
import math

default_elo_ranges = (1500, 1700, 1800, 2000)


class Tournament:
    def __init__(
        self, num_players: int, elo_ranges: tuple[int] = default_elo_ranges
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

        print(
            f"Tier Sizes: High={self.high_tier_size}, Mid={self.mid_tier_size}, Low={self.low_tier_size}"
        )

        self.players: list[Player] = []
        self.current_round = Round()

        # Generate players evenly amongst elo tiers
        for tier_size, tier_top_elo, tier_bottom_elo, tier_name in zip(
            (self.high_tier_size, self.mid_tier_size, self.low_tier_size),
            (self.top_tier_high_elo, self.top_tier_low_elo, self.mid_tier_low_elo),
            (self.top_tier_low_elo, self.mid_tier_low_elo, self.bottom_tier_low_elo),
            ("High", "Mid", "Low"),
        ):
            increment = (tier_top_elo - tier_bottom_elo) / (tier_size - 1)
            print(f"low={tier_bottom_elo}, increment={increment}")

            for i in range(tier_size):
                name = f"{tier_name}_{i}"
                self.players.append(Player(name, tier_bottom_elo + (i * increment)))

        for x in self.players:
            print(f"Name: {x.name}, Rating: {round(x.rating, 2)}")

        for player in self.players:
            bracket = player.name.split("_")[0].upper()
            self.current_round.add_player(player, Bracket[bracket])

    def give_passive_points(self):
        self.current_round.give_passive_points()

    def run_round(self):
        results = self.current_round.generate_matches_and_simulate_round()