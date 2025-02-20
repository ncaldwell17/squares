from pydantic import BaseModel, Field
from uuid import UUID, uuid4


class Square(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    color: str
    rotation: int
