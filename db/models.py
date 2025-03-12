from sqlalchemy import Integer, String, LargeBinary, TIMESTAMP, func
from datetime import datetime, timezone

from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base


class RequestHistory(Base):
    __tablename__ = "request_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    image_data: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        default=datetime.now(timezone.utc)
    )
