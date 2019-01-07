from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from celestialKitchen.database import Model
from celestialKitchen.models.drop import Drop


class Area(Model):
    __tablename__ = 'area'
    id = Column(Integer, primary_key=True, autoincrement=True)
    server_id = Column(String, ForeignKey('server.id'))
    name = Column(String)
    drops = relationship(Drop, backref="area")

    def __init__(self, server_id, name):
        self.server_id = server_id
        self.name = name
