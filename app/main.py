import utils.clients
import utils.http_session
import utils.transport
import utils.session
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List

from app.ingest import run_ingest
from app.search import search_cases, initialize_search_index

app = FastAPI(title="Mini Data Interop Service")


class SearchRequest(BaseModel):
    query: str
    top_k: int = 5


class SearchResult(BaseModel):
    case_id: int
    score: float
    title: str
    status: str


@app.on_event("startup")
def startup_event():
    initialize_search_index()


@app.post("/ingest")
def ingest(dry_run: bool = Query(default=True)):
    try:
        return run_ingest(dry_run=dry_run)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/search", response_model=List[SearchResult])
def search(request: SearchRequest):
    return search_cases(request.query, request.top_k)