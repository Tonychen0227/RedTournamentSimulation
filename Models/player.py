from typing import Iterable

class Player():
    def __init__(self, name: str, rating: int) -> None:
        self.name = name
        self.rating = rating
        self.points = 0

    def give_points(self, points: int) -> None:
        self.points += points

    def expected_score_against(self, opponent: 'Player') -> float:
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

    def expected_score_against_many(self, opponents: Iterable['Player']) -> float:
        if self.rating == 0:
            return 0

        opponents = [x for x in opponents if x.rating > 0]

        avg_opponent = Player("Average Opponent", sum([x.rating for x in opponents]) / len(opponents))

        return self.expected_score_against(avg_opponent)

    def __repr__(self):
        return f"Player({self.name}, {self.rating})"
