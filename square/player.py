from typing import Iterable
from square.enums import Bracket, PlayoffOrder


class Match:
    def __init__(self, placement: int, bracket: Bracket, num_opponents: int):
        self.placement = placement
        self.bracket = bracket
        self.num_opponents = num_opponents
        self.did_win = placement == 0
        self.did_lose = placement == num_opponents

    def __repr__(self):
        return f"Place: {self.placement + 1} in bracket {self.bracket} against {self.num_opponents} opponents"


class Player:
    def __init__(self, name: str, rating: float, points: int = 0) -> None:
        self.name = name
        self.rating = rating
        self.points = points
        self.bye_round = PlayoffOrder.NONE
        self.points_history = []
        self.match_history = []

    def give_points(self, points: int) -> None:
        # print(f"Player {self} given {points} points")

        self.points += points
        self.points_history.append(points)

    def promote_to_playoffs(self, bye_round: PlayoffOrder):
        self.bye_round = bye_round

    def expected_score_against(self, opponent: "Player") -> float:
        if self.rating == 0:
            return 0

        if opponent.rating == 0:
            return 1

        # https://www.tennisabstract.com/blog/2019/12/03/an-introduction-to-tennis-elo/
        difference = opponent.rating - self.rating
        modified_difference = difference / 400
        ten_pow_modified_difference = pow(10, modified_difference)
        one_plus_ten_pow = 1 + ten_pow_modified_difference

        return 1 / one_plus_ten_pow

    def expected_score_against_many(self, opponents: Iterable["Player"]) -> float:
        if self.rating == 0:
            return 0

        opponents = [x for x in opponents if x.rating > 0]

        avg_opponent = Player(
            "Average Opponent", sum([x.rating for x in opponents]) / len(opponents)
        )

        return self.expected_score_against(avg_opponent)

    def __repr__(self):
        return f"Player({self.name}, {round(self.rating, 2)}, POINTS={self.points})"
