"""Kullanici modeli — ana backend ile ayni tablo (kullanicilar)."""

import uuid
import enum
from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, Enum, Integer, String, Text, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.session import Base


class KullaniciRol(str, enum.Enum):
    admin     = "admin"
    abd_admin = "abd_admin"
    egitmen   = "egitmen"
    danisman  = "danisman"
    asistan   = "asistan"
    teknisyen = "teknisyen"


class Kullanici(Base):
    __tablename__ = "kullanicilar"
    id              = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organizasyon_id = Column(UUID(as_uuid=True), nullable=True)
    ad_soyad    = Column(String(120), nullable=False)
    email       = Column(String(200), unique=True, nullable=False, index=True)
    sifre_hash  = Column(String(255), nullable=False)
    rol         = Column(Enum(KullaniciRol), nullable=False, default=KullaniciRol.asistan)
    super_admin = Column(Boolean, default=False)
    aktif       = Column(Boolean, default=True)
    bildirim_tercihleri = Column(JSON, nullable=True)
    platformlar = Column(JSON, nullable=True)
    olusturma   = Column(DateTime(timezone=True), server_default=func.now())
