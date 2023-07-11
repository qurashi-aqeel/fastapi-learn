from pydantic import BaseModel

# Pydantic Post Base model
class PostBase(BaseModel):
    title: str
    content: str
    draft: bool = False

class PostCreate(PostBase):
    pass

