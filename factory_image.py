from sqlalchemy import Column, Integer, String
from base import Base


class FactoryImage(Base):
    __tablename__ = 'factory_image'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    sha256 = Column(String(250), nullable=False)
