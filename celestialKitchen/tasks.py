import asyncio
import discord
from celestialKitchen.config import config
from celestialKitchen.inventory import adjust_item_quantity


async def do_explore(client, user):
    while user.ticks > 0:
        await asyncio.sleep(config.TICK_RATE)
        if config.ENV == 'dev':
            print('{} - {}/{}'.format(user.id, user.initial_ticks - user.ticks + 1, user.initial_ticks))
        user.update(ticks=user.ticks-1)

    item = 'Rock'
    quantity = 1
    if user.initial_ticks == 3:
        item = 'Wood'
    elif user.initial_ticks == 4:
        quantity = 2
    elif user.initial_ticks == 5:
        item = 'Tin Ore'

    adjust_item_quantity(user, item, quantity)

    if quantity > 1:
        resp = '{} found {} {}s!'.format(user.mention, quantity, item)
    else:
        resp = '{} found a {}!'.format(user.mention, item)

    print(resp)
    await client.send_message(discord.Object(user.destination), resp)
    user.update(is_exploring=False, initial_ticks=0)