from celestialKitchen.database import db
from celestialKitchen.models.user import User, register_new_user
from celestialKitchen.models.item import Item
from celestialKitchen.wrappers import requires_admin, fetch_server
from celestialKitchen.schema import command, EmptySchema, IdSchema, MentionSchema, NumericSchema


@requires_admin
@command(NumericSchema)
async def process_delete_item(client, message, number):
    item = db.session.query(Item).filter_by(id=number).first()
    if not item:
        await client.send_message(message.channel, 'I can\'t find that item')
        return

    item.delete()
    await client.send_message(message.channel, '{} removed'.format(item.name))


@requires_admin
@command(MentionSchema)
async def process_force_abandon(client, message, user):
    user.update(is_exploring=False, ticks=0, initial_ticks=0)
    await client.send_message(message.channel, 'Kicked {} out of their exploration'.format(user.mention))


@requires_admin
@command(IdSchema)
async def process_force_register(client, message, id):
    user = db.session.query(User).filter_by(id=id).first()
    if user:
        await client.send_message(message.channel, 'They are already registered!'.format(user.mention))
    else:
        user = register_new_user(id, "", "", "<@{}>".format(id), message.channel)
        await client.send_message(message.channel, 'Registered {}!'.format(user.mention))


@requires_admin
@command(EmptySchema)
@fetch_server
async def process_mods(client, message, server):
    resp = '**__Mods__**'
    for mod in server.mods:
        if mod.name == mod.display_name:
            resp += '\n{}'.format(mod.name)
        else:
            resp += '\n{} _aka:_ {}'.format(mod.name, mod.display_name)
    await client.send_message(message.channel, resp)


@requires_admin
@command(MentionSchema)
@fetch_server
async def process_mod(client, message, user, server):
    mods = server.mods
    mods.append(user)
    server.update(mods=mods)
    await client.send_message(message.channel, 'Modded {}!'.format(user.mention))


@requires_admin
@command(MentionSchema)
@fetch_server
async def process_remove_mod(client, message, user, server):
    mods = server.mods
    try:
        mods.remove(user)
    except ValueError:
        await client.send_message(message.channel, '{} isn\'t a mod!'.format(user.mention))
        return
    server.update(mods=mods)
    await client.send_message(message.channel, 'Removed {}\'s mod status!'.format(user.mention))