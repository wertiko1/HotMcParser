import asyncio

from parser import VoteStatisticsFetcher

HOTMC_URL = "https://hotmc.ru/vote-XXXXXX"


async def main():
    stats_fetcher = VoteStatisticsFetcher(HOTMC_URL)

    # Получаем общее количество голосов
    total_votes = await stats_fetcher.get_total_votes()
    print(f"Total votes: {total_votes}")

    # Получаем количество голосующих игроков
    votes_count = await stats_fetcher.get_votes_count()
    print(f"Votes count: {votes_count}")

    # Получаем информацию о самых голосующих игроках
    top_voted_players = await stats_fetcher.get_top_voted_players()
    print("Top Voted Players:")
    for entry in top_voted_players:
        print(f"{entry.player_name}: {entry.vote_count}")


# Usage
if __name__ == "__main__":
    asyncio.run(main())
