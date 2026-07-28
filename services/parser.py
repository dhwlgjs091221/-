from models.game_status import GameStatus


class NoticeParser:

    def parse(self, titles: list[str]) -> GameStatus:

        status = GameStatus()

        for title in titles:

            lower = title.lower()

            if "시즌" in title or "season" in lower:
                status.season = title

            elif "추출" in title or "모집" in title or "픽업" in title:
                status.pickup = title

            elif "이벤트" in title:
                status.event = title

            elif "점검" in title:
                status.maintenance = title

            elif status.notice == "정보 없음":
                status.notice = title

        return status