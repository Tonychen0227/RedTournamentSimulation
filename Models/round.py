from Models.bracket import Bracket
from Models.player import Player


class Round:
    def __init__(self):
        self.brackets = {}

    def add_player(self, player: Player, bracket: Bracket):
        if bracket not in self.brackets.keys():
            self.brackets[bracket] = []

        self.brackets[bracket].add(player)

    def remove_player_from_bracket(self, player: Player, bracket: Bracket):
        if bracket not in self.brackets.keys():
            raise ValueError(f"Bracket {bracket} does not exist!")

        self.brackets[bracket] = [x for x in self.brackets[bracket] if x != player]

    def generate_matches(self):
        matches = []

    def give_passive_points(self):
        score_distribution = [[Bracket.HIGH, 2], [Bracket.HIGH, 1], [Bracket.HIGH, 0]]

        for combo in score_distribution:
            bracket = combo[0]
            points = combo[1]

            for player in self.brackets[bracket]:
                player.give_points(points)