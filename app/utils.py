from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)

def verify(password, hashed_password):
    return pwd_context.verify(password, hashed_password)

def post_to_dict_mod(post):
    # Forming dict manually
    return {
            "title": post[0].title,
            "id": post[0].id,
            "created_at": post[0].created_at,
            "content": post[0].content,
            "draft": post[0].draft,
            "owner_id": post[0].owner_id,
            "votes": post[1],
            "owner": {
                "email": post[0].owner.email,
                "id": post[0].owner.id,
                "created_at": post[0].owner.created_at
            }
        }
