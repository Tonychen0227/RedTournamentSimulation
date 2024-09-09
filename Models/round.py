from .bracket import Bracket
from .helpers import Helpers
from .player import Player
import random


class Round:
    def __init__(self, should_print: bool = True) -> None:
        self.brackets: dict[Bracket, list[Player]] = {}
        self.should_print = should_print

    def add_player(self, player: Player, bracket: Bracket) -> None:
        if bracket not in self.brackets.keys():
            self.brackets[bracket] = []

        if self.should_print:
            print(f"Adding {player} to bracket {bracket}")

        self.brackets[bracket].append(player)

    def remove_player_from_bracket(self, player: Player, bracket: Bracket) -> None:
        if bracket not in self.brackets.keys():
            raise ValueError(f"Bracket {bracket} does not exist!")

        self.brackets[bracket] = [x for x in self.brackets[bracket] if x != player]

    def generate_matches_and_simulate_round(self) -> dict[Bracket, list[list[Player]]]:
        matches = {
            Bracket.HIGH: [],
            Bracket.MID: [],
            Bracket.LOW: []
        }

        results = {
            Bracket.HIGH: [],
            Bracket.MID: [],
            Bracket.LOW: []
        }

        for category in [Bracket.HIGH, Bracket.MID, Bracket.LOW]:
            players = self.brackets[category]

            while len(players) > 0:
                #generate 2-man matches
                match = []

                player_1 = random.choice(players)
                players.remove(player_1)
                match.append(player_1)

                player_2 = random.choice(players)
                players.remove(player_2)
                match.append(player_2)

                player_3 = None
                if len(players) % 3 == 1:
                    player_3 = random.choice(players)
                    players.remove(player_3)
                    match.append(player_3)

                result = []

                # Simulate the match
                if len(match) == 3:
                    win_rates = Helpers.get_player_winrates(match[0], match[1], match[2])
                    roll = random.random()

                    winner = None
                    cumulative = 0
                    for x in win_rates.keys():
                        cumulative += win_rates[x]
                        if roll < cumulative:
                            winner = x
                            break

                    result.append(winner)
                    match.remove(winner)

                expected_points = match[0].expected_score_against(match[1])
                roll = random.random()
                if roll < expected_points:
                    result.append(match[0])
                    result.append(match[1])
                else:
                    result.append(match[1])
                    result.append(match[0])

                results[category].append(result)

        return results

    def give_passive_points(self):
        score_distribution = [[Bracket.HIGH, 3], [Bracket.MID, 1], [Bracket.LOW, 0]]

        for bracket, points in score_distribution:
            for player in self.brackets[bracket]:
                player.give_points(points)
