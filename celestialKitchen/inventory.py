from celestialKitchen.database import db
from celestialKitchen.models.item import Item


def adjust_item_quantity(user, name, quantity):
    if not user:
        return
    for item in user.items:
        if item.name == name:
            item.update(quantity=item.quantity + quantity, commit=False)
            if item.quantity <= 0:
                item.delete()
            else:
                item.save()
            return
    Item.create(user_id=user.id, name=name, quantity=quantity)


def check_item(user, name, quantity):
    item = db.session.query(Item).filter_by(user_id=user.id, name=name).first()
    if item:
        return item.quantity >= quantity
    return False
