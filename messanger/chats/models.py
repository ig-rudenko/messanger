from datetime import datetime

from sqlalchemy import Text, func
from sqlalchemy.orm import Mapped, mapped_column

from messanger.orm.base_model import OrmBase
from messanger.orm.manager import Manager


class Message(OrmBase, Manager):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True)
    sender_id: Mapped[int] = mapped_column(index=True)
    recipient_id: Mapped[int] = mapped_column(index=True)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), index=True)
