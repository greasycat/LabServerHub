from flask_login import UserMixin
from sqlalchemy.orm import Mapped, mapped_column

from app.database import db


class UserModel(db.Model, UserMixin):
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    email: Mapped[str] = mapped_column(db.String, unique=True, nullable=False)
    username: Mapped[str] = mapped_column(db.String, nullable=False)
    password: Mapped[str] = mapped_column(db.String, nullable=False)
