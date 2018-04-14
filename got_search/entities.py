from dataclasses import dataclass


@dataclass(frozen=True)
class Season:
    num: int
    synopsis: str


@dataclass(frozen=True)
class Episode:
    num: int
    title: str
    synopsis: str
    season: Season
