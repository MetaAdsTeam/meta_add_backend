from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, ForeignKey, Boolean

from root import models


class TimeSlot(models.Base):
    __tablename__ = 'timeslots'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    from_time = Column(DateTime, nullable=False)
    to_time = Column(DateTime, nullable=False)
    locked = Column(Boolean, nullable=False)

    def __init__(
            self,
            from_time: int,
            to_time: int,
            locked: bool,
    ):
        self.from_time = datetime.fromtimestamp(from_time)
        self.to_time = datetime.fromtimestamp(to_time)
        self.locked = locked
