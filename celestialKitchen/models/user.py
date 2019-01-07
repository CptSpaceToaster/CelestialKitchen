from sqlalchemy import Column, Boolean, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from celestialKitchen.database import Model
from celestialKitchen.models.item import Item


class User(Model):
    __tablename__ = 'user'
    id = Column(String, primary_key=True)
    name = Column(String)
    display_name = Column(String)
    items = relationship(Item, backref="user")

    mention = Column(String)
    destination = Column(String)

    is_exploring = Column(Boolean)
    initial_ticks = Column(Integer)
    drop_id = Column(Integer)
    ticks = Column(Integer)

    def __init__(self, id, name, display_name, mention=None, destination=None):
        self.id = id
        self.name = name
        self.display_name = display_name
        self.mention = mention
        self.destination = destination
        self.is_exploring = False
        self.initial_ticks = 0
        self.ticks = 0


def register_new_user(id, name, display_name, mention, destination):
    return User.create(id=id, name=name, display_name=display_name, mention=mention, destination=destination)