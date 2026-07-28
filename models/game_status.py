from dataclasses import dataclass


@dataclass
class GameStatus:

    season: str = "정보 없음"

    event: str = "정보 없음"

    pickup: str = "정보 없음"

    notice: str = "정보 없음"

    maintenance: str = "없음"