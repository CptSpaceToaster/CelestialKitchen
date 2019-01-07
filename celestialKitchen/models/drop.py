from sqlalchemy import Column, Integer, String, ForeignKey

from celestialKitchen.database import Model


class Drop(Model):
    __tablename__ = 'drop'
    id = Column(Integer, primary_key=True, autoincrement=True)
    area_id = Column(Integer, ForeignKey('area.id'))
    name = Column(String)
    quantity = Column(Integer)
    ticks = Column(Integer)
    weight = Column(Integer)

    def __init__(self, area_id, name, quantity, ticks, weight):
        self.area_id = area_id
        self.name = name
        self.quantity = quantity
        self.ticks = ticks
        self.weight = weight
