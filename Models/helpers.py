from models.player import Player


class Helpers:
    @staticmethod
    def get_player_winrates(player_1: Player, player_2: Player, player_3: Player):
        contestants = [player_1, player_2, player_3]

        rates = []

        for x in contestants:
            rates.append(x.expected_score_against_many([k for k in contestants if k != x]))

        rates_sum = sum(rates)
        rates = [k / rates_sum for k in rates]

        ret = {}

        for i in range(0, 3):
            ret[contestants[i]] = rates[i]

        return ret
