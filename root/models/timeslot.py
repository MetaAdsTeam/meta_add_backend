from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, Boolean

from root import models


class TimeSlot(models.Base):
    __tablename__ = 'timeslots'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    from_time = Column(DateTime, nullable=False)
    to_time = Column(DateTime, nullable=False)
    locked = Column(Boolean, nullable=False)

    def __init__(
            self,
            from_time: str,
            to_time: str,
            locked: bool,
    ):
        self.from_time = datetime.fromisoformat(from_time)
        self.to_time = datetime.fromisoformat(to_time)
        self.locked = locked
