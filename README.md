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
@app.post('/create')
def create(post: Post):
  return post
```

everything else will be there, such as fastApi import etc.

Now if we don't send any of the required fields in request body or send any field which can't be converted (say "a" instead of int value), it will automatically through an error with status code of 422.
