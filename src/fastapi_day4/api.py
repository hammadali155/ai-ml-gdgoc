from __future__ import annotations

from typing import Dict, List

import psycopg
from fastapi import Depends, FastAPI, Header, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from qdrant_client import QdrantClient
from sqlalchemy.orm import Session

from fastapi_day4.agent import run_agent_loop
from fastapi_day4.logging_utils import create_agent_log, create_rag_log
from fastapi_day4.rag import answer_with_rag
from fastapi_day4.schema import AgentRequest, AgentResponse, RagRequest, RagResponse
from fastapi_day4.settings import get_settings

from .db import get_db
from .models import Item

# from git_day_practice.settings import get_settings

settings = get_settings()
app = FastAPI(title=settings.app_name)


class ItemCreate(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    price: float = Field(gt=0)
    in_stock: bool = True


class ItemOut(BaseModel):
    id: int
    name: str
    price: float
    in_stock: bool


class DivideRequest(BaseModel):
    a: float
    b: float


class DivideResponse(BaseModel):
    result: float


class ErrorResponse(BaseModel):
    error_type: str
    message: str
    details: list[dict] | None = None


_items: Dict[int, ItemOut] = {}
_next_id = 1


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    _request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content=ErrorResponse(
            error_type="validation_error",
            message="Request data is invalid",
            details=exc.errors(),
        ).model_dump(),
    )


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}


@app.get("/health/ready")
def ready_health() -> dict[str, str]:
    try:
        with psycopg.connect(settings.database_url) as conn:
            conn.cursor().execute("SELECT 1;")
    except Exception as exc:
        raise HTTPException(503, detail=f"postgres not ready: {exc}") from exc
    try:
        QdrantClient(url=settings.qdrant_url).get_collections()
    except Exception as exc:
        raise HTTPException(503, detail=f"qdrant not ready: {exc}") from exc
    return {"status": "ready"}


@app.get("/db/health")
async def db_health():
    s = get_settings()
    try:
        with psycopg.connect(s.database_url) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1;")
                _ = cur.fetchone()
        return {"postgres": "ok"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"postgres not ready: {e}") from e


@app.get("/qdrant/health")
async def qdrant_health():
    s = get_settings()
    try:
        client = QdrantClient(url=s.qdrant_url)
        # A simple call that should succeed if Qdrant is reachable.
        _ = client.get_collections()
        return {"qdrant": "ok"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"qdrant not ready: {e}") from e


@app.get("/config")
async def show_config() -> dict:
    # Do NOT return secrets like API_KEY
    s = get_settings()
    return {
        "app_name": s.app_name,
        "environment": s.environment,
        "debug": s.debug,
        "host": s.host,
        "port": s.port,
        "allowed_origins": s.allowed_origins,
    }


@app.post("/items", response_model=ItemOut, status_code=201)
async def create_item(payload: ItemCreate) -> ItemOut:
    global _next_id
    item = ItemOut(id=_next_id, **payload.model_dump())
    _items[_next_id] = item
    _next_id += 1
    return item


@app.get("/items", response_model=List[ItemOut])
async def list_items() -> List[ItemOut]:
    return list(_items.values())


@app.get("/items/{item_id}", response_model=ItemOut)
async def get_item(item_id: int) -> ItemOut:
    if item_id not in _items:
        raise HTTPException(status_code=404, detail="Item not found")
    return _items[item_id]


@app.delete("/items/{item_id}", status_code=204)
async def delete_item(item_id: int) -> None:
    if item_id not in _items:
        raise HTTPException(status_code=404, detail="Item not found")
    del _items[item_id]
    return None


@app.get("/secure-data")
async def secure_data(x_api_key: str | None = Header(default=None)) -> dict:
    s = get_settings()
    if x_api_key != s.api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return {"secret_data": "approved"}


@app.post("/math/divide", response_model=DivideResponse)
async def divide(payload: DivideRequest) -> DivideResponse:
    if payload.b == 0:
        raise HTTPException(
            status_code=400,
            detail="Division by zero is not allowed",
        )
    return DivideResponse(result=payload.a / payload.b)


# --------------- DB-backed item endpoints ---------------


@app.post("/db/items", status_code=201)
async def create_db_item(payload: ItemCreate, db: Session = Depends(get_db)):  # noqa: B008
    item = Item(
        name=payload.name,
        price=payload.price,
        in_stock=payload.in_stock,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return {
        "id": item.id,
        "name": item.name,
        "price": item.price,
        "in_stock": item.in_stock,
        "created_at": item.created_at,
    }


@app.get("/db/items")
async def list_db_items(db: Session = Depends(get_db)):  # noqa: B008
    items = db.query(Item).order_by(Item.id.asc()).all()
    return [
        {
            "id": x.id,
            "name": x.name,
            "price": x.price,
            "in_stock": x.in_stock,
            "created_at": x.created_at,
        }
        for x in items
    ]


# --------------- Day 15: RAG endpoint ---------------


@app.post("/rag", response_model=RagResponse)
def rag_endpoint(payload: RagRequest, db: Session = Depends(get_db)) -> RagResponse:  # noqa: B008
    try:
        result = answer_with_rag(payload.question, payload.limit)

        if settings.enable_rag_logging:
            confidence = result["confidence"]
            create_rag_log(
                db,
                question=result["question"],
                normalized_query=result["normalized_query"],
                action=result["action"],
                reason=result["reason"],
                answer=result["answer"],
                top_score=confidence["top_score"],
                avg_score=confidence["avg_score"],
                result_count=confidence["result_count"],
            )

        return RagResponse(
            question=result["question"],
            normalized_query=result["normalized_query"],
            action=result["action"],
            reason=result["reason"],
            answer=result["answer"],
            confidence=result["confidence"],
            sources=result["sources"],
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"RAG failed: {exc}") from exc


# --------------- Day 18: Agent-RAG endpoint ---------------


@app.post("/agent-rag", response_model=AgentResponse)
def agent_rag_endpoint(
    payload: AgentRequest,
    db: Session = Depends(get_db),  # noqa: B008
) -> AgentResponse:
    try:
        result = run_agent_loop(payload.question, payload.limit)

        if settings.enable_agent_logging:
            create_agent_log(
                db,
                question=result["question"],
                normalized_query=result["normalized_query"],
                plan="\n".join(result["plan"]),
                action=result["action"],
                reason=result["reason"],
                answer=result["answer"],
            )

        return AgentResponse(
            question=result["question"],
            normalized_query=result["normalized_query"],
            plan=result["plan"],
            action=result["action"],
            reason=result["reason"],
            answer=result["answer"],
            confidence=result["confidence"],
            sources=result["sources"],
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Agent RAG failed: {exc}") from exc
