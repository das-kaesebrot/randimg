from pydantic import BaseModel


class ImageResponse(BaseModel):
    id: str
    url: str
