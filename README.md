# fastapi-learn

### Contents:

- Setup vscode and python
- References/Docs
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
- Authentication with JWT
- Allowing Only authenticated users to use certain path operations
- User specific posts
- Return owner_id as well as owner with specific post
- Search, filter and pagination
- Environment Variables
- Votes table - composite Key
- Added votes to the returned "posts" path operations
- Database migrations with Alembic
- CORS Policy
- Setting up git for fastApi projects
- Setup Docker
- Docker Compose
- Getting started with testing
- CI/CD
  - Github Actions
  - Github Marketplace

## Setup

Download the latest version of vscode and python from there official websites and install for the approprate machine.

## References/Docs

- [This Project](https://github.com/Iqueal/fastapi-learn)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Pydantic](https://docs.pydantic.dev/)
- [SwaggerUi/Docs](http://127.0.0.1:8000/docs)
- [Psucopg 2](https://www.psycopg.org/docs/index.html)
- [PostgresQL](https://www.postgresql.org/docs/)
- [SQLAlchemy](https://docs.sqlalchemy.org/en/)
- [JWT](https://jwt.io/)
- [Postgresql tutorial](https://www.postgresqltutorial.com/)
- [Alembic](https://alembic.sqlalchemy.org/)
- [DockerHub python](https://hub.docker.com/_/python)
- [Docker Compose](https://docs.docker.com/compose/)
- [Github Actions](https://docs.github.com/en/actions)
- [Github Actions Py Guide](https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-python)
- [Github Marketplace](https://github.com/marketplace)

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

## Authentication with JWT

- Inside `auth.py` create POST path operation with route `/login`

- check if:

  - user exists
  - password is correct:
    ```py
      pwd_context.verify(password, hashed_password)
    ```

- If no such user exists then return "incorrect creadentials".

- Else if user exists: Create JWT

## Allowing Only authenticated users to use certain path operations

Check:

- `verify_access_token`
- `get_current_user`
- Depends - OAuth2PasswordBearer

## User specific Posts

```py
# Get posts based on logged in user.
# This path operation has to be above GET '/{id}' otherwise it will be unreachable.
@router.get('/user', response_model=list[schemas.PostRes])
def get_user_posts(
    db: Session = Depends(get_db),
    current_user: schemas.UserRes = Depends(oauth2.get_current_user)
):
    posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    return posts

```

## Return owner_id as well as owner with specific post

```py
# models.py

    owner_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    owner = relationship("User")


# schemas.py -> below UserRes

class PostRes(PostBase):
    id: int
    owner_id: int
    created_at: datetime
    owner: UserRes

    model_config = ConfigDict(extra='forbid')

```

## Search filter and pagination

```py
# Get all posts
@router.get('/', response_model=list[schemas.PostRes])
def get_posts(
    db: Session = Depends(get_db),
    limit: int | None = None,
    skip: int | None = None,
    search: str | None = None
):
    posts = db.query(models.Post).filter(
        models.Post.title.contains(search)
        # | models.Post.content.contains(search)
        # to search 'query' from content as well.
    ).offset(skip).limit(limit).all()
    return posts

```

## Environment Variables

Reading environment variables from .env file:

```py
# config.py

from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    db_hostname: str
    db_port: str
    db_password: str
    db_name: str
    db_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache()
def get_env():
    return Settings() # type: ignore

env = get_env()

```

To get the value of env variable:

```py
from .config import env

SECRET_KEY = env.secret_key
```

> I used environment variables to create the connection string and to get secret key, algorithm, accesstoken expiry across two files `database.py` & `oauth2.py`.

## Votes table - composite Key

- Composite Key: is the primary key that spans over multiple columns. In the case of votes/likes table the composite key (primary key) is the user_id & post_id columns.

> SQL Query to grab posts with total votes:

```sql
-- All posts
  SELECT posts.*, SUM(votes.direction) AS votes
  FROM posts
  LEFT JOIN votes ON posts.id = votes.post_id
  GROUP BY posts.id;

-- Single post
  SELECT posts.*, SUM(votes.direction) AS votes
  FROM posts
  LEFT JOIN votes ON posts.id = votes.post_id
  WHERE posts.id = 17
  GROUP BY posts.id;
```

These queries will sum up all the upvotes +1 and downvotes -1 for the posts and give the result.

## Added votes to the returned "posts" path operations

New structure of posts returned

```py
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

```

SQLAlchemy query to grab posts:

```py
# All posts
posts = db.query(
    models.Post,
    func.sum(models.Vote.direction).label("votes")
  ).join(
    models.Vote,
    models.Vote.post_id == models.Post.id,
    isouter=True
  ).group_by(models.Post.id).filter(
    models.Post.title.contains(search)
  ).offset(skip).limit(limit).all()

# Single post
matched_post = db.query(
        models.Post,
        func.sum(models.Vote.direction).label("votes")
    ).join(
        models.Vote,
        models.Vote.post_id == models.Post.id,
        isouter=True
    ).group_by(models.Post.id).filter(
        models.Post.id == id
    ).first()
```

## Database migrations with Alembic

If we make changes to our database models (sqlalchemy) the changes will not be reflected only the tables will be created if they don't exist. So after making changes to models we need to delete the table and then save the code once which reloades the fastapi server resulting in creation of brand new table with all the columns and changes.

But incase we don't want to loose the existing data we use the migration tool like alembic:

```sh
pip install alembic
```

We have a few commands:

- alembic init
- alembic current
- alembic history
- alembic upgrade 'rivision'
- alembic downgrade 'rivision'
- alembic revision -m "add foreign key to post table"

Define upgrade and downgrade inside revision files:

```py
# ./alembic/versions/af786......to_posts_table.py
from alembic import op
import sqlalchemy as sa

def upgrade():
  op.add_column(
    'posts',
    sa.Column('owner_id', sa.Integer(), nullable=False)
  )
  op.create_foreign_key(
    'post_users_fk',
    source_table='posts',
    referent_table='users',
    local_cols=['owner_id'],
    remote_cols=['id'],
    ondelete='CASCADE'
  )

def downgrade():
  op.drop_constraint(
    'post_users_fk',
    table_name='posts'
  )
  op.drop_column('posts', 'owner_id')
```

## CORS Policy

- Cross Origin Resource Sharing (CORS) allows us to make requests from a web browser on one domain to a server on a different domain.

- Origin = protocol + domain + port = `http` + `localhost` + `3000`

- We might want to specify if our backend allows:

  - Requests From various domains
  - Credentials (Authorization headers, Cookies, etc).
  - Only a few HTTP methods
  - Specific HTTP headers or all of them with the wildcard "\*"

- Setting it up:

```py
from fastapi.middleware.cors import CORSMiddleware

# underneath app = FastAPI()
origins = [
    "https://www.google.com", # => google.com can talk to my api now.
    "http://localhost:8080",
]

# origins = ["*"] # = allowed from all origins.

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Setting up git for fastApi projects

- .gitignore

```
.vscode
__pycache__
venv
.env
.DS_Store
.cache
.ipynb_checkpoints
```

- Add requirements.txt to git repo

```sh
# to save requirements.txt
pip freeze > requirements.txt

# to install the same versions of depedencies
pip install -r requirements.txt
```

## Setup Docker

- Start with a Dockerfile, this is have all of the steps necessary to create our own custom image.

```Dockerfile
FROM python:3.11

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

```

- Run the following command:

```sh
# help = docker build --help
# -t, --tag = tag (what should this image be called)
# . = destination of image is current directory

docker build -t fastapi-learn .
```

- If this succceeds which it should, we can see list of docker images:

```sh
docker images ls
```

## Docker Compose

create a file `docker-compose.yml`

- see more inside `docker-compose-dev.yml` and `docker-compose-dev.yml`

- Learn more later 14:00:00.

## Getting started with testing

- Install pytest:

```sh
pip install pytest
```

- Let's create a folder in the root to test some simple functions.

- Test names should look like `test_*.py` so that `pytest` wi detect those.

- we have a simple function `test/stuffToTest/calculations.py` with a test file `test/test_calc.py`

```py
# test/stuffToTest/calculations.py
def add(a: int, b:int):
    return a + b

# test/test_calc.py
from .stuffToTest import calculations

def test_add():
    print("testing add...")
    assert calculations.add(2 ,5) == 7
```

> Naming of the functions also matters when it comes to auto discovering tests. To test `add()` we must have `test_add()` to help pytest automatically discover the corrsponding test for some function.

- To run the test:

```sh
pytest
pytest -v # verbose
pytest -s # to see print statements
```

- Use parametrize from pytest.mark to test a list of values.

## CI/CD - Continuous Integration / Continuous Delivery

create a file `.github/workflows/build-deploy.yml`:

```yml
name: Build and Deploy

on:
  push:
    branches: 
      - main
      - feature branch

jobs:
  job1:
    runs-on: ubuntu-latest
    steps:
      - name: pulling repo
        uses: actions/checkout@v3 # from marketplace
      - name: Say hi
        run: echo "hi, bro - it is awesome.."
```
