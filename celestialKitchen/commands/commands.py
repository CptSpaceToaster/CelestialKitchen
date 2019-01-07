import discord
import random
from celestialKitchen.client import config
from celestialKitchen.wrappers import fetch_user, fetch_server
from celestialKitchen.schema import command, EmptySchema, CraftSchema, AreaSchema
from celestialKitchen.tasks import do_explore


@command(AreaSchema)
@fetch_user
async def process_explore(client, message, area, user):
    if user.is_exploring:
        await client.send_message(discord.Object(user.destination), 'You are already exploring {}. Wait for your expedition in the {} to complete!'.format(user.mention, area.name))
        return

    drop = random.choice(sum(([drop] * drop.weight for drop in area.drops), []))
    print(drop.name)
    user.update(ticks=drop.ticks, initial_ticks=drop.ticks, is_exploring=True, drop_id=drop.id)

    await client.send_message(discord.Object(user.destination), '{} went exploring in the {}'.format(user.mention, area.name))
    await do_explore(client, user)


@command(EmptySchema)
@fetch_user
@fetch_server
async def process_help(client, message, user, server):
    resp = '**__Commands__**\n'
    resp += '`{}help` - Show this menu\n'.format(config.DEFAULT_COMMAND_PREFIX)
    resp += '`{}areas` - Show a list of known areas\n'.format(config.DEFAULT_COMMAND_PREFIX)
    resp += '`{}explore [area]` - Explore in an area for useful materials\n'.format(config.DEFAULT_COMMAND_PREFIX)
    resp += '`{}recipes` - Show a list of known recipes\n'.format(config.DEFAULT_COMMAND_PREFIX)
    resp += '`{}craft [recipe]` - Craft a recipe\n'.format(config.DEFAULT_COMMAND_PREFIX)
    if user in server.mods:
        resp += '\n**__Mod Commands__**\n'
        resp += '`{}inspect [@mention]` - Dump a user\'s ID and inventory information\n'.format(config.DEFAULT_COMMAND_PREFIX)
        resp += '`{}grant [@mention] [item] [quantity]` - Grant an item to a user (default quantity is 1)\n'.format(config.DEFAULT_COMMAND_PREFIX)
        resp += '`{}remove [@mention] [item] [quantity]` - Remove an item from a user\n'.format(config.DEFAULT_COMMAND_PREFIX)
        resp += '`{}add_area [area]` - Add an explorable area to the current server\n'.format(config.DEFAULT_COMMAND_PREFIX)
        resp += '`{}remove_area [area]` - Remove an area from the current server\n'.format(config.DEFAULT_COMMAND_PREFIX)
        resp += '`{}add_drop [area] [item] [quantity] [ticks] [weight]` - Add a drop to an explorable area\n'.format(config.DEFAULT_COMMAND_PREFIX)
        resp += '`{}remove_drop [area] [item]` - Remove a drop from an explorable area\n'.format(config.DEFAULT_COMMAND_PREFIX)
        resp += '`{}drops [area]` - List the drops from an explorable area\n'.format(config.DEFAULT_COMMAND_PREFIX)
        resp += '`{}set_drop_quantity [area] [item] [quantity]` - Set a drop\'s quantity\n'.format(config.DEFAULT_COMMAND_PREFIX)
        resp += '`{}set_drop_ticks [area] [item] [ticks]` - Set the number of ticks a user must wait to obtain a drop\n'.format(config.DEFAULT_COMMAND_PREFIX)
        resp += '`{}set_drop_weight [area] [item] [weight]` - Set a drop\'s weight. Higher = More Likely\n'.format(config.DEFAULT_COMMAND_PREFIX)
    await client.send_message(discord.Object(user.destination), resp)


@command(EmptySchema)
@fetch_user
@fetch_server
async def process_areas(client, message, user, server):
    resp = '**__Areas__**'
    for area in server.areas:
        resp += '\n{}'.format(area.name)
    await client.send_message(discord.Object(user.destination), resp)


@command(EmptySchema)
@fetch_user
async def process_recipes(client, message, user):
    resp = '**__Recipes__**'
    # TODO
    await client.send_message(discord.Object(user.destination), resp)


@command(EmptySchema)
@fetch_user
async def process_inv(client, message, user):
    resp = '{}\'s Inventory'.format(user.mention)
    for item in user.items:
        resp += '\n{} x{}'.format(item.name, item.quantity)
    await client.send_message(discord.Object(user.destination), resp)


@command(CraftSchema)
@fetch_user
async def process_craft(client, message, recipe, user):
    await client.send_message(discord.Object(user.destination), 'I don\'t know how to craft a {}'.format(recipe))