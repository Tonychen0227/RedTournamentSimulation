from .bracket import Bracket
from .player import Player


class Round:
    def __init__(self) -> None:
        self.brackets: dict[Bracket, list[Player]] = {}

    def add_player(self, player: Player, bracket: Bracket) -> None:
        if bracket not in self.brackets.keys():
            self.brackets[bracket] = []

        print(f"Adding player {player.name} with rating {player.rating} to bracket {bracket}")

        self.brackets[bracket].append(player)

    def remove_player_from_bracket(self, player: Player, bracket: Bracket) -> None:
        if bracket not in self.brackets.keys():
            raise ValueError(f"Bracket {bracket} does not exist!")

        self.brackets[bracket] = [x for x in self.brackets[bracket] if x != player]

    def generate_matches_and_simulate_round(self) -> None:
        matches = []

    def give_passive_points(self):
        score_distribution = [[Bracket.HIGH, 2], [Bracket.MEDIUM, 1], [Bracket.LOW, 0]]

        for bracket, points in score_distribution:
            for player in self.brackets[bracket]:
                player.give_points(points)
