from fastapi import FastAPI
from pydantic import BaseModel


# Pydantic Post model
class Post(BaseModel):
    title: str
    desc: str
    draft: bool = False
    rating: int | None = None


app = FastAPI()


@app.post('/create-post')
async def create_post(post: Post):
    print(post.model_dump())
    return post
