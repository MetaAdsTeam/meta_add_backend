from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean

from root import models


class AdSpot(models.Base):
    __tablename__ = 'adspots'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String)
    publisher_id = Column(Integer, ForeignKey('publishers.id'), nullable=False)
    spot_type_id = Column(Integer, ForeignKey('adspot_types.id'), nullable=False)
    price = Column(Float, nullable=False, default=0)
    preview_url = Column(String)
    preview_thumb_url = Column(String)
    spot_metadata = Column(String)
    publish_url = Column(String)
    stop_url = Column(String)
    jump_url = Column(String)
    default_media = Column(String)
    delay_before_publish = Column(Float, nullable=False, default=0, server_default='0')
    active = Column(Boolean, default=True)

    def __init__(
            self,
            name,
            description,
            publisher_id,
            spot_type_id,
            price,
            preview_url,
            preview_thumb_url,
            spot_metadata,
            publish_url,
            stop_url,
            jump_url,
            delay_before_publish,
    ):
        self.name = name
        self.description = description
        self.publisher_id = publisher_id
        self.spot_type_id = spot_type_id
        self.price = price
        self.preview_url = preview_url
        self.preview_thumb_url = preview_thumb_url
        self.spot_metadata = spot_metadata
        self.publish_url = publish_url
        self.stop_url = stop_url
        self.jump_url = jump_url
        self.delay_before_publish = delay_before_publish
