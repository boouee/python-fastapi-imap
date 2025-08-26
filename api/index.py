from fastapi import FastAPI, Request,Form
#from tgbot.main import tgbot
from api.imap_handler import imap_handler
from api.new_comment_handler import new_comment_handler
from urllib.parse import unquote, urlparse
from pydantic import BaseModel

class Data(BaseModel):
    ID: int

class Body(BaseModel):
    data: Data
    
app = FastAPI()

@app.get('/api/update')
async def update(request: Request):
    try:
        ...
        await imap_handler()
    except Exception as e:
        print(e)


@app.post('/api/new-comment')
async def update(request: Request):    
    try:
        form = await request.form()
        print(form)
        print(form['data[FIELDS][ID]'])
        await new_comment_handler(form['data[FIELDS][ID]'])
    except Exception as e:
        print(e)
