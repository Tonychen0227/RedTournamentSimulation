from square.enums import Bracket, PlayoffOrder
from square.enums import TournamentStage
from square.helper import simulate_match
from square.player import Player
import random


class Tournament:
    def __init__(self,
                 min_elo: int = 800,
                 max_elo: int = 1900,
                 num_players: int = 0,
                 tournament_stage: TournamentStage = TournamentStage.BRACKETS_ASSIGNED_MATCHES_PENDING,
                 override_players: list[Player] = None):
        self.state = tournament_stage
        self.matches = {}
        self.player_brackets = {Bracket.ASCENSION: [], Bracket.REGULAR: []}
        self.matches = {Bracket.ASCENSION: [], Bracket.REGULAR: []}

        if override_players is not None:
            self.players = override_players

            for player in self.players:
                self.player_brackets[Bracket.REGULAR].append(player)

            return

        increment = (max_elo - min_elo) / (num_players - 1)
        players = []

        for i in range(0, num_players):
            players.append(Player(f"Player{i}", min_elo + (increment*i)))

        self.players = players

        for player in self.players:
            self.player_brackets[Bracket.REGULAR].append(player)

    def assign_matches(self):
        if self.state != TournamentStage.BRACKETS_ASSIGNED_MATCHES_PENDING:
            raise ValueError(f"assign_matches not supported in the current state")

        matches = {}
        for bracket in self.player_brackets.keys():
            matches[bracket] = []
            players = self.player_brackets[bracket]

            random.shuffle(players)

            while len(players) % 3 != 0:
                matches[bracket].append([players.pop(), players.pop()])

            while len(players) > 0:
                matches[bracket].append([players.pop() for _ in range(0, 3)])

        self.matches = matches
        self.player_brackets = {Bracket.ASCENSION: [], Bracket.REGULAR: []}
        self.state = TournamentStage.MATCHES_ASSIGNED_RESULTS_PENDING

    def run_matches(self,
                    ascension_mid_points: int,
                    ascension_bottom_points: int,
                    regular_top_points: int,
                    regular_mid_points: int,
                    regular_bottom_points: int,
                    next_playoff_order: PlayoffOrder):
        if self.state != TournamentStage.MATCHES_ASSIGNED_RESULTS_PENDING or len(self.matches.keys()) == 0:
            raise ValueError(f"run_matches not supported in the current state")

        player_brackets = {Bracket.ASCENSION: [], Bracket.REGULAR: []}

        # run ascension
        ascension_matches = self.matches[Bracket.ASCENSION]
        next_playoff_order = next_playoff_order

        for match in ascension_matches:
            results = simulate_match(match)

            # winner moves on to playoffs
            results[0].promote_to_playoffs(next_playoff_order)

            # loser drops down to regular
            results[-1].give_points(ascension_bottom_points)
            player_brackets[Bracket.REGULAR].append(results[-1])

            if len(results) == 3:
                results[1].give_points(ascension_mid_points)
                player_brackets[Bracket.ASCENSION].append(results[1])

        # run regular
        regular_matches = self.matches[Bracket.REGULAR]
        for match in regular_matches:
            results = simulate_match(match)

            results[0].give_points(regular_top_points)
            player_brackets[Bracket.ASCENSION].append(results[0])

            results[-1].give_points(regular_bottom_points)
            player_brackets[Bracket.REGULAR].append(results[-1])

            if len(results) == 3:
                results[1].give_points(regular_mid_points)
                player_brackets[Bracket.REGULAR].append(results[1])

        self.player_brackets = player_brackets
        self.state = TournamentStage.BRACKETS_ASSIGNED_MATCHES_PENDING

    def get_top_cut(self, size_of_cut: int = 27):
        top_cut = []

        top_cut.extend([x for x in self.players if x.bye_round == PlayoffOrder.FIRST])
        top_cut.extend([x for x in self.players if x.bye_round == PlayoffOrder.SECOND])
        top_cut.extend([x for x in self.players if x.bye_round == PlayoffOrder.THIRD])

        last_seen_score = -1
        no_playoffs_bye = [x for x in sorted(self.players, key=lambda player: player.points, reverse=True) if x.bye_round == PlayoffOrder.NONE]

        for remaining_player in no_playoffs_bye:
            if len(top_cut) < size_of_cut:
                top_cut.append(remaining_player)
                last_seen_score = remaining_player.points
            elif remaining_player.points == last_seen_score:
                top_cut.append(remaining_player)

        return top_cut, last_seen_score
