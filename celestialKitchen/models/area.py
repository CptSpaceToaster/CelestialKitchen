from sqlalchemy import Column, String, ForeignKey

from celestialKitchen.database import Model


class Area(Model):
    __tablename__ = 'area'
    id = Column(String, primary_key=True)
    name = Column(String)
    server_id = Column(String, ForeignKey('server.id'))

    def __init__(self, id, name):
        self.id = id
        self.name = name
