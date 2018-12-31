from sqlalchemy import Column, Integer, String, ForeignKey

from celestialKitchen.database import Model


class Item(Model):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey('user.id'))
    name = Column(String)
    quantity = Column(Integer)

    def __init__(self, user_id, name, quantity):
        self.user_id = user_id
        self.name = name
        self.quantity = quantity
