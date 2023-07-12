# fastapi-learn

### Contents:

- Setup vscode and python
- Creating virtual environment
  - Creating the virtual env in windows
  - Creating the virtual env in mac
- Installing FastAPI
- Start coding the basic api
  - Creating first path operation
  - Post request path operation
- Download and install postgresql
- Create DB, table and write SQL quries
- Connecting to DB from app
  - Retreving data from DB
  - Creating a post
- Using SQLAlchemy
  - Install sqlAlchemy and setup conn & models
  - Qureying DB
- Defining response Model
- Password Hashing with passlib
- routers (keeping route based code seperated)

## Setup

Download the latest version of vscode and python from there official websites and install for the approprate machine.

## Virtual env

We can seperate the different versions of pyhton packages for the different projects, it doesn't effect the the global installations of packages, keeping the version in isolation with the current project.

### Creating the virtual env in windows

Enter this command in the terminal (cmd or powershell) to create a virtual env with name venv:

```sh
py -3 -m venv venv
```

A folder named venv will be created.

Now select the python interpritter which is inside that folder.

`ctrl + p` > select interpritter > enter path > `.\venv\Scripts\python.exe`

It should now use this interpritter everytime we open this project but still double check everytime (at the bottom of vscode) if the correct interpritter is selected.

We want our terminal to use the same interpritter as well, so enter this command:

```sh
venv\Scripts\activate.bat
```

Now we see the name of virtual env in the beginning of the pathname inside the terminal.

### Creating the virtual env in mac

command:

```sh
python3 -m venv venv
```

`cmd + p` > select interpritter > enter path > `./venv/Scripts/python`

for terminal:

```sh
source venv/bin/activate
```

## Installing FastAPI

First of all spin up the [fastApi docs tutorial](https://fastapi.tiangolo.com/tutorial/), copy the installation command. To install fastapi with all its necessary dependencies we need to enter the following (or copied) command:

```sh
pip install "fastapi[all]"
```

## Start coding the basic api

### Creating first path operation

Import fastApi:

```py
# import FastAPI class
from fastapi import FastAPI

# create instance of it
app = FastAPI()

# create route (path operation)

# path operation decorator
@app.get('/')
# path operation function
def root():
    return {'message': 'Hello World'}
```

To start the app we need to type this command:

`uvcorn <name of file>:<name of the instance> --reload`

```sh
uvicorn main:app --reload
```

Reload flag in the command watches the app for any change, so we are using this flag only during development not in production.

> Note: The order in which the path operations are created matters, so if we create two path operations with same path (say "/") the first one is going to get executed.

So now our app is started at [localhost](http://127.0.0.1:8000/), we can visit this url and see what we returned from path operation function.

We also have the docs avaliable to us at [Swagger UI](http://127.0.0.1:8000/docs), so we can choose between the lots of options we have such as this swagger ui, thunder client, postman etc.

### Post request path operation

```py
@app.post('/create-post')
def create_post():
    return {"create": "post"}
```

- Validation of the data passed as response to the path operation can be done using pydantic, here is how:

```py
from pydantic import BaseModel

# Pydantic Post model
class Post(BaseModel):
  title: str
  desc: str
  draft: bool = False # default value false
  rating: int | None = None # Optional, defaults to None


# create a post path operation:
@app.post('/create', status_code=status.HTTP_201_CREATED) # default status code for path op.
def create(post: Post):
  return post
```

everything else will be there, such as fastApi import etc.

Now if we don't send any of the required fields in request body or send any field which can't be converted (say "a" instead of int value), it will automatically through an error with status code of 422.

- To keep everything organized we will create a folder named app which changes our command to:

```sh
uvicorn app.main:app --reload
```

telling python to find the main file inside app folder.

## Download and install postgresql

Download the specific version of the postgresql software from official website, install and setup a password, which will be the root password.

## Create DB, table and write SQL quries

There should be an existing DB `postgres` which you could use but let's create something else with our preferred name `fastapi` it might ask for some password give it a password and we are ready to create a table.

Go inside `databases` > `fastapi` > `schemas` > `public` > `tables`.

Create table `products` with few columns `id, name etc`.

Here is an SQL query which might describe various basic things for getting the data from DB.

```sql
  SELECT id, name, price, created_at, in_stock,
  inventory AS quantity /* Rename inventory as quantity */
  FROM products
  WHERE name NOT LIKE '%b%' /* Something as prefic and sufix of 'b' */
  AND ( /* Match this as well (anyone from below) OR */
    inventory >= 5
    OR name = 'tv'
    OR id IN (1, 9, 10)
  ) ORDER BY created_at DESC, price /* Sort by latest first */
  OFFSET 0 /* Skip as many entries */
  LIMIT 10; /* Limit the entries to 10 */
```

- Limit and offset will be used for pagination.

Inserting data to DB

```sql
  INSERT INTO products (
    name, price, inventory
  ) VALUES (
    'macbook', 500, 3
  ), (
    'monitor', 70, 17
  ) RETURNING id, name; /* * to return all fields */
```

Disclaimer: This is advanced usecase:
If we want some column dependent on another we can use the triggers in postgress as:

```sql

CREATE OR REPLACE FUNCTION set_in_stock()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.inventory > 0 THEN
        NEW.in_stock := true;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER set_in_stock_trigger
BEFORE INSERT ON products
FOR EACH ROW
EXECUTE FUNCTION set_in_stock();

```

This query will set a trigger that whenever anything is inserted into the database or anything is added to it it will update the `in_Stock` as per the value of `inventory`, if the inventory is 0, it will set the `in_stock` to false else true.

Alter Table:

```sql
  ALTER TABLE products
  ADD CONSTRAINT in_stock_check
  CHECK (inventory > 0 AND in_stock = true);
```

Update table data:

```sql
  UPDATE products
  SET name='brush', price=12
  WHERE id=10
  RETURNING id, name;
```

Delete:

```sql
  DELETE FROM products
  WHERE name = 'chair'
  RETURNING *;
```

## connecting to DB from app

```py

while True:
    try:
        conn = psycopg.connect(
            host="localhost", dbname="fastapi-learn",
            user="postgres", password="password"
        )
        print("DB connected.")
        cur = conn.cursor(row_factory=dict_row)

        break

    except Exception as error:
        print("Failed connecting to DB", error)
        time.sleep(2)

```

### Retreving data from DB

```py
# Get all posts
@app.get('/posts')
def get_posts():
    posts = cur.execute("SELECT * FROM posts").fetchall()
    return {"data": posts}

```

### Creating a post DB

```py
# Create a post
@app.post('/posts', status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):
    new_post = cur.execute(
        f"INSERT INTO posts (title, content, draft) VALUES (%s, %s, %s) RETURNING *", (post.title, post.content, post.draft)).fetchone()
    conn.commit()
    return {"data": new_post}
```

## Install sqlAlchemy and setup conn & models

- conn. string format: `postgresql://<username>:<password>@<ip-address/hostname/domain>/<DB_name>`

- Install sqlAlchemy: `pip install sqlalchemy`

- database.py

```py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_CONN_STRING = 'postgresql://postgres:password@localhost/fastapi-learn'

engine = create_engine(DATABASE_CONN_STRING)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

```

- models.py

```py
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

from .database import Base


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    draft = Column(Boolean, server_default='FALSE')
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))

```

### Qureying DB

```py
# Getting data
@app.get('/posts')
def test(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}
```

```py
# Posting/Inserting data
@app.post('/posts', status_code=status.HTTP_201_CREATED)
async def create_post(post: Post, db: Session = Depends(get_db)):
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {"data": new_post}
```

- Normally we would pass the arguments to the `models.Post()` as `title=post.title, content=post.content, draft=post.draft` but there is an easier and consize way of doing the same:

  - Convert the post to dict using `post.model_dump()`.
  - Convert the post_dict to required format `title=post.title,..` prefixing it with `**`.
  - pass it `**post.model_dump()` as the argument to the `models.Post()`
  - Or simply we can say that `**post.model_dump()` unpacks the values.

- Get, Post, Put, Del

```py
# GET
posts = db.query(models.Post).all()

# POST
new_post = models.Post(**post.model_dump())
db.add(new_post)
db.commit()
db.refresh(new_post)

# GET One
matched_post = db.query(models.Post).filter(models.Post.id == id).first()

# DEL
matched_post = db.query(models.Post).filter(
  models.Post.id == id
).delete(synchronize_session=False)
db.commit()

# PUT
post_query = db.query(models.Post).filter(models.Post.id == id)
    post_to_update = post_query.first()

if (post_to_update):
    post_query.update(dict(post.model_dump()), synchronize_session=False)
    db.commit()
    return {"Updated post": post_query.first()}
```

## Defining response Model

Response Model:

```py
from pydantic import ConfigDict

class PostRes(PostBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(extra='forbid')


# List of posts
@app.get('/posts', response_model=list[PostRes]) # list
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


# Single Post
@app.get(
    '/posts/{id}',
    status_code=status.HTTP_200_OK,
    response_model=PostRes # Single post dict.
)...
```

## Password Hashing with passlib

Install passlib:

```sh
pip install "passlib[bcrypt]"
```

Create user with hashed password

```py
# utils.py - hash password utility function
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def hash(password: str):
    return pwd_context.hash(password)


# main.py
# Creating User
@app.post(
    "/users",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.UserRes
)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    # Hash the passwoed
    user.password = hash(user.password)

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

```

## routers (keeping route based code seperated)

- Routers help us to seperate the path operation logic outside of our main.py, so that it remains cleaner.

- So we create a routers folder inside which we create 3 files:

  - `__init__.py`: making it the subpackage.
  - `post.py`: includes post related routes.
  - `user.py`: includes user related routes.

- Now we can organize our routes as well as SwaggerUi better:

  - inside `post.py` we do something like this:

  ```py
    from fastapi import APIRouter

    router = APIRouter(
      prefix='/posts',
      tags=["Posts"] 
      # This will group the post related requests under 'Posts' title.
    )
  ```
