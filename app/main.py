from fastapi import FastAPI, Depends, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .config import settings
from .database import Base, engine, get_db
from . import crud, schemas
from .websocket_manager import ConnectionManager
from .stats import RealTimeStats

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.FRONTEND_ORIGINS + ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ws_manager = ConnectionManager()
rt_stats = RealTimeStats()

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/api/events/order", response_model=schemas.OrderOut)
def ingest_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    db_order = crud.create_order(db, order)
    rt_stats.update_from_order(db_order)
    import asyncio
    asyncio.create_task(ws_manager.broadcast(rt_stats.to_payload_dict()))
    return db_order

@app.websocket("/ws/dashboard")
async def websocket_dashboard(websocket: WebSocket):
    await ws_manager.connect(websocket)
    try:
        await websocket.send_json(rt_stats.to_payload_dict())
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)