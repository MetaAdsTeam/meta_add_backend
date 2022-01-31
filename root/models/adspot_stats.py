from sqlalchemy import Column, Integer, String, ForeignKey

from root import models


class AdSpotsStats(models.Base):
    __tablename__ = 'adspots_stats'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    spot_id = Column(Integer, ForeignKey('adspots.id'))
    likes = Column(Integer)
    views_amount = Column(Integer)
    average_time = Column(Integer)
    max_traffic = Column(Integer)

    def __init__(
            self,
            spot_id,
            likes,
            views_amount,
            average_time,
            max_traffic,
    ):
        self.spot_id = spot_id
        self.likes = likes
        self.views_amount = views_amount
        self.average_time = average_time
        self.max_traffic = max_traffic
