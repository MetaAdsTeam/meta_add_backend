from sqlalchemy import Column, Integer, String, ForeignKey, Boolean

from root import models


class TimeSlot(models.Base):
    __tablename__ = 'timeslots'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    adspot_id = Column(Integer)
    from_time = Column(Integer)
    to_time = Column(Integer)
    locked = Column(Boolean)

    def __init__(
            self,
            adspot_id,
            from_time,
            to_time,
            locked,
    ):
        self.adspot_id = adspot_id
        self.from_time = from_time
        self.to_time = to_time
        self.locked = locked
