import traceback
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.router import api_router
from app.db.session import engine, Base

# Tablolari olustur
from app.models import kullanici, sinav  # noqa: F401
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sinav Otomasyon API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    tb = traceback.format_exc()
    print(f"HATA: {request.method} {request.url}\n{tb}")
    return JSONResponse(status_code=500, content={"detail": str(exc), "traceback": tb})


app.include_router(api_router)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/debug/tables")
def debug_tables():
    from sqlalchemy import inspect
    inspector = inspect(engine)
    return {"tables": inspector.get_table_names()}
