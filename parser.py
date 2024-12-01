from typing import List, Optional

from aiohttp import ClientSession
from bs4 import BeautifulSoup

from models import VoteEntry


class HtmlFetcher:
    def __init__(self, url: str) -> None:
        self.url = url

    async def fetch_html(self) -> str:
        async with ClientSession() as session:
            async with session.get(self.url) as response:
                return await response.text()


class VoteStatisticsFetcher:
    def __init__(self, url: str) -> None:
        self._url = url
        self.html_content: Optional[str] = None

    async def fetch_html_data(self) -> None:
        fetcher = HtmlFetcher(self._url)
        self.html_content = await fetcher.fetch_html()

    async def get_total_votes(self) -> str:
        if self.html_content is None:
            await self.fetch_html_data()

        soup = BeautifulSoup(self.html_content, 'html.parser')
        vote_count_element = soup.find('span', class_='count')
        return vote_count_element.text if vote_count_element else "0"

    async def get_votes_count(self) -> int:
        if self.html_content is None:
            await self.fetch_html_data()

        soup = BeautifulSoup(self.html_content, 'html.parser')
        table = soup.find('table', class_='table')

        if table is None:
            print("Error: Table with class 'table' not found.")
            return 0

        player_names = [
            row.find_all('td')[0].text.strip()
            for row in table.find_all('tr')
            if len(row.find_all('td')) >= 2
        ]
        return len(player_names)

    async def get_top_voted_players(self) -> List[VoteEntry]:
        if self.html_content is None:
            await self.fetch_html_data()

        soup = BeautifulSoup(self.html_content, 'html.parser')
        table = soup.find('table', class_='table')

        if table is None:
            print("Error: Table with class 'table' not found.")
            return []

        vote_entries = [
            VoteEntry(vote_count=int(columns[1].text.strip()), player_name=columns[0].text.strip())
            for row in table.find_all('tr')
            if (columns := row.find_all('td')) and len(columns) >= 2
        ]
        return vote_entries
