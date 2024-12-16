from fastapi.responses import HTMLResponse, JSONResponse
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

from model.model_api import load_model, load_embeddings, get_most_similar, load_data

app = FastAPI()
templates = Jinja2Templates(directory="templates")

model = load_model()
embeddings = load_embeddings()
articles = load_data()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/search")
async def search(request: Request):
    query = request.query_params.get("query")
    if query is None:
        return JSONResponse(content={"error": "No query provided"}, status_code=400)
    most_similar = get_most_similar(query, embeddings, model, articles)
    return JSONResponse(content={"response_test": most_similar})
