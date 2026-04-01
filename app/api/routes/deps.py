"""Ortak FastAPI bagimliliklari."""

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.kullanici import Kullanici
from app.core.security import decode_access_token

oauth2 = OAuth2PasswordBearer(tokenUrl="/api/v2/auth/giris", auto_error=True)

# ─── Rol gruplari ───
ADMIN_ROLLER = {"admin", "abd_admin"}
OGRETIM_UYESI_ROLLER = {"egitmen", "danisman"}
YETKILI_ROLLER = ADMIN_ROLLER | OGRETIM_UYESI_ROLLER


def get_user(token: str = Depends(oauth2), db: Session = Depends(get_db)) -> Kullanici:
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(401, "Gecersiz oturum")
    u = db.query(Kullanici).filter_by(id=payload["sub"]).first()
    if not u or not u.aktif:
        raise HTTPException(401, "Kullanici bulunamadi")
    return u


def get_yetkili_user(user: Kullanici = Depends(get_user)) -> Kullanici:
    """Admin veya ogretim uyesi olmalidir."""
    rol = user.rol.value if hasattr(user.rol, 'value') else str(user.rol)
    if rol not in YETKILI_ROLLER and not user.super_admin:
        raise HTTPException(403, "Bu islemi yapmaya yetkiniz yok. Sadece admin ve ogretim uyeleri erisebilir.")
    return user


def get_admin_user(user: Kullanici = Depends(get_user)) -> Kullanici:
    """Sadece admin olmalidir."""
    rol = user.rol.value if hasattr(user.rol, 'value') else str(user.rol)
    if rol not in ADMIN_ROLLER and not user.super_admin:
        raise HTTPException(403, "Bu islemi sadece yoneticiler yapabilir.")
    return user


def is_admin(user: Kullanici) -> bool:
    rol = user.rol.value if hasattr(user.rol, 'value') else str(user.rol)
    return rol in ADMIN_ROLLER or user.super_admin
