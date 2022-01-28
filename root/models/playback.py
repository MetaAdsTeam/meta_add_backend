from sqlalchemy import Column, Integer, String, ForeignKey, Boolean

from root import models


class Playback(models.Base):
    __tablename__ = 'playbacks'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    adspot_id = Column(Integer)
    timeslot_id = Column(Integer)
    advert_id = Column(Integer)
    content_id = Column(Integer)
    status_id = Column(Integer)
    smart_contract = Column(String)

    def __init__(
            self,
            adspot_id,
            timeslot_id,
            advert_id,
            content_id,
            status_id,
            smart_contract,
    ):
        self.adspot_id = adspot_id
        self.timeslot_id = timeslot_id
        self.advert_id = advert_id
        self.content_id = content_id
        self.status_id = status_id
        self.smart_contract = smart_contract
