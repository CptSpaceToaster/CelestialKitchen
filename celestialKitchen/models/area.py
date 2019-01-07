from sqlalchemy import Column, Integer, String, ForeignKey

from celestialKitchen.database import Model


class Area(Model):
    __tablename__ = 'area'
    id = Column(Integer, primary_key=True, autoincrement=True)
    server_id = Column(String, ForeignKey('server.id'))
    name = Column(String)

    def __init__(self, server_id, name):
        self.server_id = server_id
        self.name = name
