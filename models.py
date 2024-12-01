from pydantic import BaseModel


class VoteEntry(BaseModel):
    vote_count: int
    player_name: str
