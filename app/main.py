from typing import List, Optional
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session
from app import models
from app.database import SessionLocal, init_db
from contextlib import asynccontextmanager

# Schemas
class TodoCreate(BaseModel):
    title: str

class TodoRead(BaseModel):
    id: int
    title: str
    done: bool
    model_config = ConfigDict(from_attributes=True)

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None

# App setup
@asynccontextmanager
async def lifespan(app):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Routes
@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/todos", response_model=List[TodoRead])
def list_todos(db: Session = Depends(get_db)):
    return db.query(models.Todo).order_by(models.Todo.id).all()

@app.post("/todos", response_model=TodoRead, status_code=201)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    item = models.Todo(title=todo.title, done=False)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@app.put("/todos/{todo_id}", response_model=TodoRead)
async def update_todo(todo_id: int, updated: Optional[TodoUpdate] = None, request: Request = None, db: Session = Depends(get_db)):
    # Accept Optional body; if Pydantic didn't parse (None) try reading raw JSON
    if updated is None and request is not None:
        try:
            body = await request.json()
        except Exception:
            body = {}
        if isinstance(body, dict) and body:
            updated = TodoUpdate(**body)

    item = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Todo not found")
    if updated is not None:
        if updated.title is not None:
            item.title = updated.title
        if updated.done is not None:
            item.done = updated.done
        db.commit()
        db.refresh(item)
    return item

@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    item = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(item)
    db.commit()
    return

# Utility: Ensure DB/tables exist when module is imported (helps tests and direct imports)
try:
    init_db()
except Exception:
    # if DB cannot be created at import (rare), skip — startup will ensure creation
    pass