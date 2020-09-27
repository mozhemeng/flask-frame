from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func

from appname.extentions import db


class TimeColumnMixin:
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class BaseModel(db.Model, TimeColumnMixin):
    __abstract__ = True

    def save(self):
        db.session.add(self)
        db.session.commit()
        db.session.refresh(self)

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        res = {}

        for col in self.__table__.columns:
            res[col.name] = getattr(self, col.name)

        return res
