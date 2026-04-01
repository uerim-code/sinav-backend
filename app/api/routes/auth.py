"""Auth endpoint — sadece giris. Kayit ana backend'den yapilir."""

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.kullanici import Kullanici
from app.core.security import verify_password, create_access_token
from app.api.routes.deps import get_user

router = APIRouter(tags=["Auth"])


@router.post("/auth/giris")
def giris(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    u = db.query(Kullanici).filter_by(email=form.username).first()
    if not u or not verify_password(form.password, u.sifre_hash):
        raise HTTPException(401, "Hatali e-posta veya sifre")
    if not u.aktif:
        raise HTTPException(403, "Hesap devre disi")
    token = create_access_token({"sub": str(u.id)})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/benim-profilim")
def profil(me: Kullanici = Depends(get_user)):
    return {
        "id": str(me.id),
        "ad_soyad": me.ad_soyad,
        "email": me.email,
        "rol": me.rol.value if me.rol else None,
        "super_admin": me.super_admin or False,
    }
