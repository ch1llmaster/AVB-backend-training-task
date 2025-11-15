from datetime import datetime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class URLBase(Base):
    __tablename__ = "url_base"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    default_url: Mapped[str] = mapped_column(nullable=False)
    uniq_id: Mapped[str] = mapped_column(nullable=False, unique=True)
    shortened_url: Mapped[str] = mapped_column(nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now,
        onupdate=datetime.now,
        nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now, nullable=False)
