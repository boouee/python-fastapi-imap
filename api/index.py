from fastapi import FastAPI, Request
#from tgbot.main import tgbot
from api.imap_handler import imap_handler
from api.new_comment_handler import new_comment_handler
from urllib.parse import unquote, urlparse
from pydantic import BaseModel

class Body(BaseModel):
    data: Data

class Data(BaseModel):
    ID: int
    
app = FastAPI()

@app.get('/api/update')
async def update(request: Request):
    try:
        ...
        await imap_handler()
    except Exception as e:
        print(e)


@app.post('/api/new-comment')
async def update(body: Body):
    print(body)
    try:
        ...
        await new_comment_handler(body["data"]["ID"])
    except Exception as e:
        print(e)
