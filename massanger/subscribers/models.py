from datetime import datetime

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.sql.functions import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..auth.models import User
from ..orm.base_model import OrmBase
from ..orm.manager import Manager


class Friendship(OrmBase, Manager):
    __tablename__ = "friendships"
    __table_args__ = (UniqueConstraint("user_id", "friend_id"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    friend_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
