from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Float, DateTime

from root import models


class Playback(models.Base):
    __tablename__ = 'playbacks'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    adspot_id = Column(Integer, ForeignKey('adspots.id'), nullable=False)
    timeslot_id = Column(Integer, ForeignKey('timeslots.id'), nullable=False)
    creative_id = Column(Integer, ForeignKey('creatives.id'), nullable=False)
    status_id = Column(Integer, ForeignKey('playback_statuses.id'))
    smart_contract = Column(String)
    play_price = Column(Float)
    taken_at = Column(DateTime)
    processed_at = Column(DateTime)

    def __init__(
            self,
            adspot_id,
            timeslot_id,
            creative_id,
            status_id,
            smart_contract,
            play_price,
            processed_at,
    ):
        self.adspot_id = adspot_id
        self.timeslot_id = timeslot_id
        self.creative_id = creative_id
        self.status_id = status_id
        self.smart_contract = smart_contract
        self.play_price = play_price
        self.processed_at = processed_at
