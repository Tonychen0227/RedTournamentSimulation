from enum import Enum


class PlayoffOrder(Enum):
    NONE = -1
    FIRST = 0
    SECOND = 1
    THIRD = 2


class Bracket(Enum):
    REGULAR = 0
    ASCENSION = 1


class TournamentStage(Enum):
    BRACKETS_ASSIGNED_MATCHES_PENDING = 0
    MATCHES_ASSIGNED_RESULTS_PENDING = 1
