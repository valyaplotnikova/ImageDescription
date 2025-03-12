from pydantic import BaseModel


class SRequestHistory(BaseModel):
    image_data: bytes
    description: str
