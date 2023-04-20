# Creators:
# JJS
# SSR
# Import libraries
from fastapi import FastAPI, Request, File, HTTPException, UploadFile
import os
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import Body
from typing import List

# Creation of fastApi app
app = FastAPI()
# Templates is for working with html files in /templates forder
templates = Jinja2Templates(directory="templates")
# We need to mount a folder for our files (images, audio, videos), staticFiles will do it
app.mount("/static", StaticFiles(directory="static"), name="static")
# The root route will send to the user the html file


@app.get("/", response_class=HTMLResponse)
async def get_login(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/graph")
async def language_changed(value: str = Body()):
    from grafo import graphCreation
    graphCreation(value)


@app.delete("/delete-file")
async def delete_file(file_path: str = Body()):
    try:
        os.remove(file_path)
        return {"message": "File deleted successfully."}
    except Exception as e:
        return {"error": str(e)}


@app.get("/check", response_class=HTMLResponse)
async def get_login(request: Request):
    return templates.TemplateResponse("check.html", {"request": request})


@app.post("/list")
async def post_list(strings: List[str]):
    global checked
    from grafo import checkSentence
    checked = checkSentence(strings[0], strings[1:])
    # function(sentence:strings[0],matrix:strings[1:])
    return {'Value': checked}
