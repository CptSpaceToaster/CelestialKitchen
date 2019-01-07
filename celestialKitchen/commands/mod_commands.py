from celestialKitchen.database import db
from celestialKitchen.models.area import Area
from celestialKitchen.models.drop import Drop
from celestialKitchen.wrappers import requires_mod, fetch_server
from celestialKitchen.schema import command, NameSchema, MentionSchema, GrantSchema, AreaSchema, DropsSchema, NewDropSchema, RemoveDropSchema, AdjustDropSchema
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


@requires_mod
@command(NewDropSchema)
async def process_add_drop(client, message, area, name, quantity, ticks, weight):
    Drop.create(area_id=area.id, name=name, quantity=quantity, ticks=ticks, weight=weight)
    await client.send_message(message.channel, 'Registered {} in {}'.format(name, area.name))


@requires_mod
@command(RemoveDropSchema)
async def process_remove_drop(client, message, area, name):
    for drop in area.drops:
        if drop.name.lower() == name.lower():
            drop.delete()
            await client.send_message(message.channel, 'Removed {} in {}'.format(name, area.name))
            return
    await client.send_message(message.channel, 'I couldn\'t find {} in {}'.format(name, area.name))


@requires_mod
@command(DropsSchema)
async def process_drops(client, message, area, show_command):
    resp = '**__Drops - {}__**:'.format(area.name)
    for drop in area.drops:
        resp += '\n{} - quantity: {} - ticks: {} - weight: {}'.format(drop.name, drop.quantity, drop.ticks, drop.weight)
    if show_command:
        resp += '```'
        for drop in area.drops:
            resp += '\n!add_drop {} "{}" {} {} {}'.format(area.name, drop.name, drop.quantity, drop.ticks, drop.weight)
        resp += '```'
    await client.send_message(message.channel, resp)


@requires_mod
@command(AdjustDropSchema)
async def process_set_drop_quantity(client, message, area, name, number):
    for drop in area.drops:
        if drop.name.lower() == name.lower():
            drop.update(quantity=number)
            await client.send_message(message.channel, 'Set {} quantity in {} to {}'.format(name, area.name, number))
            return
    await client.send_message(message.channel, 'I couldn\'t find {} in {}'.format(name, area.name))


@requires_mod
@command(AdjustDropSchema)
async def process_set_drop_ticks(client, message, area, name, number):
    for drop in area.drops:
        if drop.name.lower() == name.lower():
            drop.update(ticks=number)
            await client.send_message(message.channel, 'Set {} ticks in {} to {}'.format(name, area.name, number))
            return
    await client.send_message(message.channel, 'I couldn\'t find {} in {}'.format(name, area.name))


@requires_mod
@command(AdjustDropSchema)
async def process_set_drop_weight(client, message, area, name, number):
    for drop in area.drops:
        if drop.name.lower() == name.lower():
            drop.update(weight=number)
            await client.send_message(message.channel, 'Set {} weight in {} to {}'.format(name, area.name, number))
            return
    await client.send_message(message.channel, 'I couldn\'t find {} in {}'.format(name, area.name))