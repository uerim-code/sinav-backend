"""
Sinav Otomasyon modelleri.
Tablo isimleri so_ prefix'li — ana backend tablolariyla cakismasin diye.
"""

import uuid
from datetime import datetime
from sqlalchemy import (
    Boolean, Column, DateTime, Date, Float, Integer, String, Text, JSON,
    ForeignKey, UniqueConstraint
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.session import Base


class Fakulte(Base):
    __tablename__ = "so_fakulteler"
    id    = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ad    = Column(String(200), nullable=False)
    aktif = Column(Boolean, default=True)

    programlar = relationship("Program", back_populates="fakulte", cascade="all, delete-orphan")


class Program(Base):
    __tablename__ = "so_programlar"
    id         = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fakulte_id = Column(UUID(as_uuid=True), ForeignKey("so_fakulteler.id", ondelete="CASCADE"), nullable=False)
    ad         = Column(String(200), nullable=False)
    aktif      = Column(Boolean, default=True)

    fakulte  = relationship("Fakulte", back_populates="programlar")
    donemler = relationship("Donem", back_populates="program", cascade="all, delete-orphan")


class Donem(Base):
    __tablename__ = "so_donemler"
    id         = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    program_id = Column(UUID(as_uuid=True), ForeignKey("so_programlar.id", ondelete="CASCADE"), nullable=False)
    ad         = Column(String(100), nullable=False)
    aktif      = Column(Boolean, default=True)

    program = relationship("Program", back_populates="donemler")
    dersler = relationship("Ders", back_populates="donem", cascade="all, delete-orphan")


class Ders(Base):
    __tablename__ = "so_dersler"
    id            = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    donem_id      = Column(UUID(as_uuid=True), ForeignKey("so_donemler.id", ondelete="CASCADE"), nullable=False)
    ad            = Column(String(200), nullable=False)
    haftalik_saat = Column(Integer, nullable=True)
    aktif         = Column(Boolean, default=True)

    donem    = relationship("Donem", back_populates="dersler")
    konular  = relationship("Konu", back_populates="ders", cascade="all, delete-orphan")
    sinavlar = relationship("Sinav", back_populates="ders", cascade="all, delete-orphan")
    kazanimlar = relationship("DersKazanim", back_populates="ders", cascade="all, delete-orphan")


class Konu(Base):
    __tablename__ = "so_konular"
    id         = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ders_id    = Column(UUID(as_uuid=True), ForeignKey("so_dersler.id", ondelete="CASCADE"), nullable=False)
    ad         = Column(String(300), nullable=False)
    hafta      = Column(Integer, nullable=True)
    saat       = Column(Integer, nullable=True)
    anlatan_id = Column(UUID(as_uuid=True), nullable=True)
    sira       = Column(Integer, nullable=True)

    ders    = relationship("Ders", back_populates="konular")
    sorular = relationship("Soru", back_populates="konu", cascade="all, delete-orphan")
    sinav_planlari = relationship("SinavPlani", back_populates="konu")
    iliskili_soru_gruplari = relationship("IliskiliSoruGrup", back_populates="konu", cascade="all, delete-orphan")
    kazanim_iliskileri = relationship("KazanimKonu", back_populates="konu")


class Soru(Base):
    __tablename__ = "so_sorular"
    id                    = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    konu_id               = Column(UUID(as_uuid=True), ForeignKey("so_konular.id", ondelete="CASCADE"), nullable=False)
    soru_metni            = Column(Text, nullable=False)
    soru_tipi             = Column(String(20), nullable=False)
    bilgisel_duzey        = Column(String(30), nullable=True)
    zorluk                = Column(String(20), nullable=True)
    kei                   = Column(Float, nullable=True)
    kgi                   = Column(Float, nullable=True)
    cevaplama_suresi      = Column(Integer, nullable=True)
    baslangic_tarihi      = Column(Date, nullable=True)
    bitis_tarihi          = Column(Date, nullable=True)
    anahtar_kelimeler     = Column(JSON, nullable=True)
    kaynakca              = Column(Text, nullable=True)
    yapilandirilmis_cevap = Column(Text, nullable=True)
    olusturan_id          = Column(UUID(as_uuid=True), ForeignKey("kullanicilar.id"), nullable=True)
    olusturuldu           = Column(DateTime(timezone=True), server_default=func.now())

    konu       = relationship("Konu", back_populates="sorular")
    secenekler = relationship("SoruSecenegi", back_populates="soru", cascade="all, delete-orphan")
    sinav_tipleri  = relationship("SoruSinavTipi", back_populates="soru", cascade="all, delete-orphan")
    cikabirlikler  = relationship("Cikabirlik", back_populates="soru", cascade="all, delete-orphan")
    sinav_sorulari = relationship("SinavSorusu", back_populates="soru")
    ogrenci_cevaplari = relationship("OgrenciCevap", back_populates="soru")


class SoruSecenegi(Base):
    __tablename__ = "so_soru_secenekleri"
    id            = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    soru_id       = Column(UUID(as_uuid=True), ForeignKey("so_sorular.id", ondelete="CASCADE"), nullable=False)
    secenek_metni = Column(Text, nullable=False)
    dogru         = Column(Boolean, default=False)
    sira          = Column(Integer, nullable=True)

    soru = relationship("Soru", back_populates="secenekler")


class SoruSinavTipi(Base):
    __tablename__ = "so_soru_sinav_tipleri"
    id         = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    soru_id    = Column(UUID(as_uuid=True), ForeignKey("so_sorular.id", ondelete="CASCADE"), nullable=False)
    sinav_tipi = Column(String(30), nullable=False)

    soru = relationship("Soru", back_populates="sinav_tipleri")


class Cikabirlik(Base):
    __tablename__ = "so_cikabirlik"
    id      = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    soru_id = Column(UUID(as_uuid=True), ForeignKey("so_sorular.id", ondelete="CASCADE"), nullable=False)
    tur     = Column(String(30), nullable=False)

    soru = relationship("Soru", back_populates="cikabirlikler")


class IliskiliSoruGrup(Base):
    __tablename__ = "so_iliskili_soru_gruplari"
    id        = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    kok_metin = Column(Text, nullable=False)
    konu_id   = Column(UUID(as_uuid=True), ForeignKey("so_konular.id", ondelete="CASCADE"), nullable=True)

    konu    = relationship("Konu", back_populates="iliskili_soru_gruplari")
    sorular = relationship("IliskiliSoru", back_populates="grup", cascade="all, delete-orphan")


class IliskiliSoru(Base):
    __tablename__ = "so_iliskili_sorular"
    id      = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    grup_id = Column(UUID(as_uuid=True), ForeignKey("so_iliskili_soru_gruplari.id", ondelete="CASCADE"), nullable=False)
    soru_id = Column(UUID(as_uuid=True), ForeignKey("so_sorular.id", ondelete="CASCADE"), nullable=False)

    grup = relationship("IliskiliSoruGrup", back_populates="sorular")
    soru = relationship("Soru")


class Sinav(Base):
    __tablename__ = "so_sinavlar"
    id               = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ders_id          = Column(UUID(as_uuid=True), ForeignKey("so_dersler.id", ondelete="CASCADE"), nullable=False)
    ad               = Column(String(300), nullable=False)
    sinav_turu       = Column(String(30), nullable=False)
    sinav_kategorisi = Column(String(30), nullable=True)
    baslangic        = Column(DateTime(timezone=True), nullable=True)
    bitis            = Column(DateTime(timezone=True), nullable=True)
    tam_puan         = Column(Integer, nullable=True)
    soru_sayisi      = Column(Integer, nullable=True)
    kitapcik_turu    = Column(Text, nullable=True)
    soru_secim_sekli = Column(String(30), nullable=True)
    olusturan_id     = Column(UUID(as_uuid=True), ForeignKey("kullanicilar.id"), nullable=True)
    durum            = Column(String(20), default="taslak")
    kilitli          = Column(Boolean, default=False)  # Sonuc yuklendikten sonra kilitlenir

    ders           = relationship("Ders", back_populates="sinavlar")
    planlar        = relationship("SinavPlani", back_populates="sinav", cascade="all, delete-orphan")
    sinav_sorulari = relationship("SinavSorusu", back_populates="sinav", cascade="all, delete-orphan")
    ogrenciler     = relationship("Ogrenci", back_populates="sinav", cascade="all, delete-orphan")
    sonuclar       = relationship("Sonuc", back_populates="sinav", cascade="all, delete-orphan")


class SinavPlani(Base):
    __tablename__ = "so_sinav_planlari"
    id           = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sinav_id     = Column(UUID(as_uuid=True), ForeignKey("so_sinavlar.id", ondelete="CASCADE"), nullable=False)
    konu_id      = Column(UUID(as_uuid=True), ForeignKey("so_konular.id", ondelete="CASCADE"), nullable=False)
    hafta        = Column(Integer, nullable=True)
    saat         = Column(Integer, nullable=True)
    gerekli_soru = Column(Integer, nullable=True)
    secilen_soru = Column(Integer, nullable=True)

    sinav = relationship("Sinav", back_populates="planlar")
    konu  = relationship("Konu", back_populates="sinav_planlari")


class SinavSorusu(Base):
    __tablename__ = "so_sinav_sorulari"
    id       = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sinav_id = Column(UUID(as_uuid=True), ForeignKey("so_sinavlar.id", ondelete="CASCADE"), nullable=False)
    soru_id  = Column(UUID(as_uuid=True), ForeignKey("so_sorular.id", ondelete="CASCADE"), nullable=False)
    sira     = Column(Integer, nullable=True)
    kitapcik = Column(String(1), nullable=True)
    # Soru snapshot — sinav uygulandiktan sonra kaydedilir
    soru_metni_snapshot   = Column(Text, nullable=True)
    secenekler_snapshot   = Column(JSON, nullable=True)  # [{"harf":"A","metin":"...","dogru":true}, ...]
    zorluk_snapshot       = Column(String(20), nullable=True)
    bilgisel_duzey_snapshot = Column(String(30), nullable=True)

    sinav = relationship("Sinav", back_populates="sinav_sorulari")
    soru  = relationship("Soru", back_populates="sinav_sorulari")


class Ogrenci(Base):
    __tablename__ = "so_ogrenciler"
    id         = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ogrenci_no = Column(Text, nullable=False)
    ad         = Column(Text, nullable=False)
    sinav_id   = Column(UUID(as_uuid=True), ForeignKey("so_sinavlar.id", ondelete="CASCADE"), nullable=False)

    sinav    = relationship("Sinav", back_populates="ogrenciler")
    sonuclar = relationship("Sonuc", back_populates="ogrenci", cascade="all, delete-orphan")


class Sonuc(Base):
    __tablename__ = "so_sonuclar"
    id         = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sinav_id   = Column(UUID(as_uuid=True), ForeignKey("so_sinavlar.id", ondelete="CASCADE"), nullable=False)
    ogrenci_id = Column(UUID(as_uuid=True), ForeignKey("so_ogrenciler.id", ondelete="CASCADE"), nullable=False)
    ham_puan   = Column(Float, nullable=True)
    net        = Column(Float, nullable=True)
    dogru      = Column(Integer, nullable=True)
    yanlis     = Column(Integer, nullable=True)
    bos        = Column(Integer, nullable=True)
    yuzdelik   = Column(Float, nullable=True)
    kitapcik   = Column(String(1), nullable=True)

    sinav    = relationship("Sinav", back_populates="sonuclar")
    ogrenci  = relationship("Ogrenci", back_populates="sonuclar")
    cevaplar = relationship("OgrenciCevap", back_populates="sinav_sonucu", cascade="all, delete-orphan")


class OgrenciCevap(Base):
    __tablename__ = "so_ogrenci_cevaplari"
    id              = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sinav_sonucu_id = Column(UUID(as_uuid=True), ForeignKey("so_sonuclar.id", ondelete="CASCADE"), nullable=False)
    soru_id         = Column(UUID(as_uuid=True), ForeignKey("so_sorular.id", ondelete="CASCADE"), nullable=False)
    verilen_secenek = Column(Text, nullable=True)
    dogru           = Column(Boolean, nullable=True)

    sinav_sonucu = relationship("Sonuc", back_populates="cevaplar")
    soru         = relationship("Soru", back_populates="ogrenci_cevaplari")


# ---------------------------------------------------------------------------
# Ders Ogrenim Kazanimi
# ---------------------------------------------------------------------------
class DersKazanim(Base):
    __tablename__ = "so_ders_kazanimlari"
    id           = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ders_id      = Column(UUID(as_uuid=True), ForeignKey("so_dersler.id", ondelete="CASCADE"), nullable=False)
    kod          = Column(String(20), nullable=False)
    aciklama     = Column(Text, nullable=False)
    bloom_duzeyi = Column(String(30), nullable=True)
    sira         = Column(Integer, nullable=True)

    ders    = relationship("Ders", back_populates="kazanimlar")
    konular = relationship("KazanimKonu", back_populates="kazanim", cascade="all, delete-orphan")


class KazanimKonu(Base):
    __tablename__ = "so_kazanim_konulari"
    id         = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    kazanim_id = Column(UUID(as_uuid=True), ForeignKey("so_ders_kazanimlari.id", ondelete="CASCADE"), nullable=False)
    konu_id    = Column(UUID(as_uuid=True), ForeignKey("so_konular.id", ondelete="CASCADE"), nullable=False)

    kazanim = relationship("DersKazanim", back_populates="konular")
    konu    = relationship("Konu", back_populates="kazanim_iliskileri")


class SoruKazanim(Base):
    """Soru — Kazanim dogrudan iliskisi (Bologna sureci)."""
    __tablename__ = "so_soru_kazanimlari"
    id         = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    soru_id    = Column(UUID(as_uuid=True), ForeignKey("so_sorular.id", ondelete="CASCADE"), nullable=False)
    kazanim_id = Column(UUID(as_uuid=True), ForeignKey("so_ders_kazanimlari.id", ondelete="CASCADE"), nullable=False)


# ══════════════════════════════════════════════════════════════════
#  BILDIRIMLER
# ══════════════════════════════════════════════════════════════════

class Bildirim(Base):
    __tablename__ = "so_bildirimler"
    id            = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    kullanici_id  = Column(UUID(as_uuid=True), ForeignKey("kullanicilar.id", ondelete="CASCADE"), nullable=False)
    baslik        = Column(String(300), nullable=False)
    mesaj         = Column(Text, nullable=True)
    tip           = Column(String(50), nullable=False, default="bilgi")  # bilgi, uyari, basari, hata
    okundu        = Column(Boolean, default=False)
    link          = Column(String(500), nullable=True)  # tıklanınca gidilecek sayfa
    olusturma     = Column(DateTime(timezone=True), server_default=func.now())
