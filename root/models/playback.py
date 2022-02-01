from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Float

from root import models


class Playback(models.Base):
    __tablename__ = 'playbacks'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    adspot_id = Column(Integer, ForeignKey('adspots.id'))
    timeslot_id = Column(Integer, ForeignKey('timeslots.id'))
    creative_id = Column(Integer, ForeignKey('creatives.id'))
    status_id = Column(Integer, ForeignKey('playback_statuses.id'))
    smart_contract = Column(String)
    play_price = Column(Float)

    def __init__(
            self,
            adspot_id,
            timeslot_id,
            creative_id,
            status_id,
            smart_contract,
            play_price,
    ):
        self.adspot_id = adspot_id
        self.timeslot_id = timeslot_id
        self.creative_id = creative_id
        self.status_id = status_id
        self.smart_contract = smart_contract
        self.play_price = play_price
