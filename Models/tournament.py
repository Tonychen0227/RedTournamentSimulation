from .bracket import Bracket
from .player import Player
from .round import Round
import math


class Tournament:
    TOP_TIER_HIGH_ELO = 2000
    TOP_TIER_LOW_ELO = 1800
    MID_TIER_LOW_ELO = 1700
    BOTTOM_TIER_LOW_ELO = 1500

    def __init__(self, num_players: int) -> None:
        self.high_tier_count = math.ceil(num_players / 3)
        num_players -= self.high_tier_count

        self.mid_tier_count = math.ceil(num_players / 2)
        num_players -= self.mid_tier_count

        self.low_tier_count = num_players

        print(f"Counts: High={self.high_tier_count}, Mid={self.mid_tier_count}, Low={self.low_tier_count}")

        self.players = []
        self.current_round = Round()

        for x in [
            [self.high_tier_count, self.TOP_TIER_HIGH_ELO, self.TOP_TIER_LOW_ELO, "High"],
            [self.mid_tier_count, self.TOP_TIER_LOW_ELO, self.MID_TIER_LOW_ELO, "Mid"],
            [self.low_tier_count, self.MID_TIER_LOW_ELO, self.BOTTOM_TIER_LOW_ELO, "Low"]
        ]:
            low = x[2]
            increment = (x[1] - x[2]) / (x[0] - 1)

            print(low, increment)

            for i in range(0, x[0]):
                name = f"{x[3]}{i}"
                self.players.append(Player(name, low + (i * increment)))

        for x in self.players:
            print(f"Name {x.name}, Rating {round(x.rating, 2)}")

        for i in range(0, self.high_tier_count):
            self.current_round.add_player(self.players[i], Bracket.HIGH)

        for i in range(0, self.mid_tier_count):
            self.current_round.add_player(self.players[self.high_tier_count + i], Bracket.MEDIUM)

        for i in range(0, self.low_tier_count):
            self.current_round.add_player(self.players[self.high_tier_count + self.mid_tier_count + i], Bracket.LOW)
