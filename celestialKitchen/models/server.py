from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Table

from celestialKitchen.database import Model
from celestialKitchen.models.area import Area
from celestialKitchen.models.user import User


mod_association_table = \
    Table('mod_association',
          Model.metadata,
          Column('server_id', Integer, ForeignKey('server.id')),
          Column('user_id', Integer, ForeignKey('user.id'))
)


class Server(Model):
    __tablename__ = 'server'
    id = Column(String, primary_key=True)
    areas = relationship(Area, backref="area")
    mods = relationship(User, secondary=mod_association_table)

    def __init__(self, id):
        self.id = id
