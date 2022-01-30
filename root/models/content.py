from sqlalchemy import Column, Integer, String, LargeBinary, ForeignKey

from root import models


class Content(models.Base):
    __tablename__ = 'contents'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    advert_id = Column(Integer, nullable=False)
    content_type_id = Column(Integer, ForeignKey('content_types.id'))
    nft_ref = Column(String, nullable=False)
    nft_bin = Column(LargeBinary, nullable=False)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)

    def __init__(
            self,
            advert_id,
            content_type_id,
            nft_ref,
            nft_bin,
            name,
            url,
    ):
        self.advert_id = advert_id
        self.content_type_id = content_type_id
        self.nft_ref = nft_ref
        self.nft_bin = nft_bin
        self.name = name
        self.url = url
