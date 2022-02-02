from sqlalchemy import Column, Integer, String, ForeignKey, Boolean

from root import models


class TimeSlot(models.Base):
    __tablename__ = 'timeslots'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    from_time = Column(Integer, nullable=False)
    to_time = Column(Integer, nullable=False)
    locked = Column(Boolean, nullable=False)

    def __init__(
            self,
            from_time,
            to_time,
            locked,
    ):
        self.from_time = from_time
        self.to_time = to_time
        self.locked = locked if isinstance(locked, bool) else locked.lower() != 'false'
