from datetime import datetime
from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.expression import false, true
from sqlalchemy.sql.functions import func

from ..orm.manager import Manager
from ..orm.base_model import OrmBase


class User(OrmBase, Manager):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(150), unique=True)
    first_name: Mapped[Optional[str]] = mapped_column(String(150))
    last_name: Mapped[Optional[str]] = mapped_column(String(150))
    email: Mapped[Optional[str]] = mapped_column(String(254), unique=True)
    password: Mapped[str] = mapped_column(String(128))
    last_login: Mapped[Optional[datetime]] = mapped_column()
    is_superuser: Mapped[bool] = mapped_column(server_default=false())
    is_staff: Mapped[bool] = mapped_column(server_default=false())
    is_active: Mapped[bool] = mapped_column(server_default=true())
    date_join: Mapped[datetime] = mapped_column(server_default=func.now())

    my_friends = relationship("Friendship", foreign_keys="[Friendship.user_id]", backref="user")
    friends_of = relationship("Friendship", foreign_keys="[Friendship.friend_id]", backref="friend")
