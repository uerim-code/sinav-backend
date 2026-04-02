import traceback
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.router import api_router
from app.db.session import engine, Base

# Tablolari olustur
from app.models import kullanici, sinav  # noqa: F401
Base.metadata.create_all(bind=engine)

# Eksik sutunlari ekle (migration)
def _migrate():
    from sqlalchemy import text
    with engine.connect() as conn:
        migrations = [
            ("so_sinavlar", "kilitli", "ALTER TABLE so_sinavlar ADD COLUMN IF NOT EXISTS kilitli BOOLEAN DEFAULT FALSE"),
            ("so_sinav_sorulari", "soru_metni_snapshot", "ALTER TABLE so_sinav_sorulari ADD COLUMN IF NOT EXISTS soru_metni_snapshot TEXT"),
            ("so_sinav_sorulari", "secenekler_snapshot", "ALTER TABLE so_sinav_sorulari ADD COLUMN IF NOT EXISTS secenekler_snapshot JSON"),
            ("so_sinav_sorulari", "zorluk_snapshot", "ALTER TABLE so_sinav_sorulari ADD COLUMN IF NOT EXISTS zorluk_snapshot VARCHAR(20)"),
            ("so_sinav_sorulari", "bilgisel_duzey_snapshot", "ALTER TABLE so_sinav_sorulari ADD COLUMN IF NOT EXISTS bilgisel_duzey_snapshot VARCHAR(30)"),
        ]
        for tablo, sutun, sql in migrations:
            try:
                conn.execute(text(sql))
                conn.commit()
            except Exception:
                conn.rollback()
try:
    _migrate()
except Exception as e:
    print(f"Migration uyarisi: {e}")

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
