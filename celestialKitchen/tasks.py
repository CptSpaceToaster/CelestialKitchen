import asyncio
import discord
from celestialKitchen.config import config
from celestialKitchen.database import db
from celestialKitchen.inventory import adjust_item_quantity
from celestialKitchen.models.drop import Drop


async def do_explore(client, user):
    while user.ticks > 0:
        await asyncio.sleep(config.TICK_RATE)
        if config.ENV == 'dev':
            print('{} - {}/{}'.format(user.id, user.initial_ticks - user.ticks + 1, user.initial_ticks))
        user.update(ticks=user.ticks-1)

    drop = db.session.query(Drop).get(user.drop_id)
    if not drop:
        await client.send_message(discord.Object(user.destination), '{} found nothing.')
        return
    adjust_item_quantity(user, drop.name, drop.quantity)

    if drop.quantity > 1:
        resp = '{} found {} {}s!'.format(user.mention, drop.quantity, drop.name)
    else:
        resp = '{} found a {}!'.format(user.mention, drop.name)

    print(resp)
    await client.send_message(discord.Object(user.destination), resp)
    user.update(is_exploring=False, initial_ticks=0)