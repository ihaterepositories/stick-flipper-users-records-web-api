from pydantic import BaseModel

class UserRecord(BaseModel):
    username: str
    bestscore: int