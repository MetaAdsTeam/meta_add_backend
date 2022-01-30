from sqlalchemy import Column, Integer, String, LargeBinary, ForeignKey

from root import models


class Creative(models.Base):
    __tablename__ = 'creatives'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    advert_id = Column(Integer, ForeignKey('advertisers.id'))
    creative_type_id = Column(Integer, ForeignKey('creative_types.id'))
    nft_ref = Column(String, nullable=False)
    nft_bin = Column(LargeBinary, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String)
    url = Column(String, nullable=False)

    def __init__(
            self,
            advert_id,
            content_type_id,
            nft_ref,
            nft_bin,
            name,
            description,
            url,
    ):
        self.advert_id = advert_id
        self.content_type_id = content_type_id
        self.nft_ref = nft_ref
        self.nft_bin = nft_bin
        self.name = name
        self.description = description
        self.url = url
