from celestialKitchen.database import db
from celestialKitchen.models.area import Area
from celestialKitchen.wrappers import requires_mod, fetch_server
from celestialKitchen.schema import command, NameSchema, MentionSchema, GrantSchema, AreaSchema
from celestialKitchen.inventory import adjust_item_quantity


@requires_mod
@command(MentionSchema)
async def process_inspect(client, message, user):
    resp = '```id: {}\n\nInventory:'.format(user.id)
    for item in user.items:
        resp += '\n{} x{} id: {}'.format(item.name, item.quantity, item.id)
    resp += '```'
    await client.send_message(message.channel, resp)


@requires_mod
@command(GrantSchema)
async def process_grant(client, message, user, name, quantity):
    adjust_item_quantity(user, name, quantity)
    await client.send_message(message.channel, 'Granted {} {}'.format(quantity, name))


@requires_mod
@command(GrantSchema)
async def process_remove(client, message, user, name, quantity):
    adjust_item_quantity(user, name, -quantity)
    await client.send_message(message.channel, 'Removed {} {} from {}'.format(quantity, name, user.mention))


@requires_mod
@command(NameSchema)
@fetch_server
async def process_add_area(client, message, name, server):
    area = db.session.query(Area).filter(Area.name.ilike(name)).first()
    if area:
        await client.send_message(message.channel, 'An area with the name {} already exists'.format(name))
    else:
        Area.create(server_id=server.id, name=name)
        await client.send_message(message.channel, 'Registered {}'.format(name))


@requires_mod
@command(AreaSchema)
async def process_remove_area(client, message, area):
    area.delete()
    await client.send_message(message.channel, 'Removed {}'.format(area.name))

