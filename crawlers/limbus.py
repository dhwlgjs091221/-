import datetime
import re
import aiohttp

STEAM_URL = "https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=1973530&count=20&maxlength=0&l=korean"


class LimbusCrawler:

    async def get_steam_news(self):
        """스팀 뉴스를 수집합니다."""
        headers = {
            "Accept-Language": "ko-KR,ko;q=0.9",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        }
        try:
            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.get(STEAM_URL) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("appnews", {}).get("newsitems", [])
        except Exception as e:
            print(f"[Steam News Fetch Error] {e}")
        return []

    def clean_bbcode(self, text):
        """스팀 전용 BBCode 태그([img], [h3] 등)를 제거합니다."""
        if not text:
            return ""
        text = re.sub(
            r"\[/?(?:img|h1|h2|h3|b|i|u|url|code|list|\*)[^\]]*\]",
            "",
            text,
            flags=re.IGNORECASE,
        )
        return text.strip()

    def parse_date(self, timestamp):
        """Unix 타임스탬프를 읽기 쉬운 한국 날짜로 변환합니다."""
        try:
            dt = datetime.datetime.fromtimestamp(
                timestamp, tz=datetime.timezone.utc
            )
            # KST 기준 (+9시간)
            kst_dt = dt + datetime.timedelta(hours=9)
            return kst_dt.strftime("%Y.%m.%d %H:%M")
        except Exception:
            return "일시 정보 없음"

    async def get_status(self):
        steam_news = await self.get_steam_news()

        events = []
        pickups = []
        updates = []
        other = []

        for item in steam_news:
            raw_title = item.get("title", "")
            title = self.clean_bbcode(raw_title)
            url = item.get("url", "")
            date_str = self.parse_date(item.get("date", 0))

            news_data = {
                "title": title,
                "url": url,
                "date": date_str,
            }

            lower = title.lower()

            # 1. 픽업 / 추출 공지
            if any(
                k in lower
                for k in ["extraction", "identity", "e.g.o", "ego", "추출"]
            ):
                pickups.append(news_data)

            # 2. 주요 이벤트 공지
            elif any(
                k in lower
                for k in [
                    "walpurgis",
                    "railway",
                    "dungeon",
                    "발푸르기스",
                    "철도",
                    "던전",
                    "시즌",
                    "복각",
                    "이벤트",
                ]
            ):
                events.append(news_data)

            # 3. 점검 및 패치 공지
            elif any(
                k in lower
                for k in [
                    "update",
                    "maintenance",
                    "hotfix",
                    "patch",
                    "점검",
                    "업데이트",
                    "패치",
                    "issues",
                ]
            ):
                updates.append(news_data)

            # 4. 기타 공지
            else:
                other.append(news_data)

        return {
            "events": events,
            "pickups": pickups,
            "updates": updates,
            "other": other,
        }