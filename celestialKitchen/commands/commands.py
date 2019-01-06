import discord
import random
from celestialKitchen.client import config
from celestialKitchen.wrappers import fetch_user
from celestialKitchen.schema import command, EmptySchema, CraftSchema
from celestialKitchen.tasks import do_explore


@command(EmptySchema)
@fetch_user
# async def process_explore(client, message, area, user):
async def process_explore(client, message, user):
    if user.is_exploring:
        await client.send_message(discord.Object(user.destination), 'You are already exploring {}. Wait for your expedition to complete!'.format(user.mention))
        return

    ticks = random.randint(1, 5)
    user.update(ticks=ticks, initial_ticks=ticks, is_exploring=True)
    await client.send_message(discord.Object(user.destination), '{} went exploring in the {}'.format(user.mention, 'TODO'))
    await do_explore(client, user)


@command(EmptySchema)
@fetch_user
async def process_help(client, message, user):
    resp = '`{}help` - Show this menu\n'.format(config.DEFAULT_COMMAND_PREFIX)
    resp += '`{}areas` - Show a list of known areas\n'.format(config.DEFAULT_COMMAND_PREFIX)
    resp += '`{}explore [area]` - Explore in an area for useful materials\n'.format(config.DEFAULT_COMMAND_PREFIX)
    resp += '`{}recipes` - Show a list of known recipes\n'.format(config.DEFAULT_COMMAND_PREFIX)
    resp += '`{}craft [recipe]` - Craft a recipe\n'.format(config.DEFAULT_COMMAND_PREFIX)
    await client.send_message(discord.Object(user.destination), resp)


@command(EmptySchema)
@fetch_user
async def process_areas(client, message, user):
    resp = '**__Areas__**'
    # TODO
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
    if recipe.craft(user):
        if recipe.output_quantity > 1:
            resp = '{} crafted {} {}s'.format(user.mention, recipe.output_quantity, recipe.output)
        else:
            resp = '{} crafted a {}'.format(user.mention, recipe.output)
    else:
        resp = 'You do not the required materials to craft a {}'.format(recipe.output)
    await client.send_message(discord.Object(user.destination), resp)