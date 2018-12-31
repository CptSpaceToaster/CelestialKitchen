import functools
import sys
import random
import asyncio

import discord

from celestialKitchen.config import get_config
from celestialKitchen.database import db
from celestialKitchen.models.server import Server
from celestialKitchen.models.user import User
from celestialKitchen.models.item import Item
from celestialKitchen.schema import command, EmptySchema, MentionSchema, NumericSchema, GrantSchema

client = discord.Client()
config = get_config()
command_prefix = config.DEFAULT_COMMAND_PREFIX


@client.event
async def on_ready():
    print('Logged in as: {} - {}'.format(client.user.name, client.user.id))
    for server in client.servers:
        if not db.session.query(Server).filter_by(id=server.id).count():
            print('  Registering {}'.format(server.id))
            Server.create(id=server.id)
        else:
            print('  Already registered {}'.format(server.id))
    print('------\nChecking to see if there are any Explorations to resume')

    for user in db.session.query(User).filter(User.ticks > 0):
        print('  Resuming exploration for {}'.format(user.id))
        asyncio.ensure_future(do_explore(client, user))
    print('------')


@client.event
async def on_message(message):
    # await do(message)
    if not message.content.startswith(command_prefix) or message.author.bot:
        return
    tokens = message.content.split(' ')
    function_name = 'process_' + tokens.pop(0).lstrip(command_prefix)

    # Shoddy token clumping
    parsed_tokens = []
    join_mode = False
    joined_token = ''
    for t in tokens:
        if t.endswith('"'):
            joined_token += ('' if t.startswith('"') else ' ') + t.lstrip('"').rstrip('"')
            join_mode = False
            parsed_tokens.append(joined_token)
            joined_token = ''
        elif t.startswith('"'):
            joined_token += t.lstrip('"')
            join_mode = True
        elif join_mode:
            joined_token += ' ' + t
        else:
            parsed_tokens.append(t)
    if join_mode:
        parsed_tokens.append(joined_token)

    try:
        func = getattr(sys.modules[__name__], function_name)
    except AttributeError:
        pass
    else:
        try:
            if config.ENV == 'dev':
                print(function_name, parsed_tokens)
            await func(client, message, tokens=parsed_tokens)
        except Exception as e:
            print('Problem in handler {} - {}'.format(function_name, message.content))
            raise e


def fetch_user(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        message = args[1]
        user = None
        if isinstance(message, discord.Message):
            author = message.author
            user = db.session.query(User).filter_by(id=author.id).first()
            if not user:
                print('Registering new user: {} {}'.format(author, author.id))
                user = User.create(id=author.id, name=author.name, display_name=author.display_name, mention=author.mention, destination=message.channel.id)
            else:
                user.update(name=author.name, display_name=author.display_name, mention=author.mention, destination=message.channel.id)
        kwargs['user'] = user
        return await func(*args, **kwargs)
    return wrapper


def requires_admin(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        message = args[1]
        if isinstance(message, discord.Message):
            author = message.author
            if author.id in config.ADMINS:
                return await func(*args, **kwargs)
            return await client.send_message(message.channel, 'You don\'t have permissions to use that command')
    return wrapper


def add_item(user, name, quantity):
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


@command(EmptySchema)
@fetch_user
async def process_explore(client, message, user):
    if not user:
        return

    if user.is_exploring:
        await client.send_message(discord.Object(user.destination), 'You are already exploring {}. Wait for your expedition to complete!'.format(user.mention))
        return

    ticks = random.randint(1, 5)
    user.update(ticks=ticks, initial_ticks=ticks, is_exploring=True)
    await client.send_message(discord.Object(user.destination), '{} went exploring'.format(user.mention))
    await do_explore(client, user)


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

    add_item(user, item, quantity)

    if quantity > 1:
        resp = '{} found {} {}s!'.format(user.mention, quantity, item)
    else:
        resp = '{} found a {}!'.format(user.mention, item)

    print(resp)
    await client.send_message(discord.Object(user.destination), resp)
    user.update(is_exploring=False, initial_ticks=0)


@command(EmptySchema)
@fetch_user
async def process_inv(client, message, user):
    if not user:
        return
    author = message.author
    resp = '{}\'s Inventory'.format(author.mention)
    for item in user.items:
        resp += '\n{} x{}'.format(item.name, item.quantity)
    await client.send_message(discord.Object(user.destination), resp)


@command(EmptySchema)
async def process_dump(client, message):
    author = message.author
    resp = '```name: {}\nid: {}\ndisplay_name: {}\n```'.format(author.name, author.id, author.display_name)
    await client.send_message(message.channel, resp)


@requires_admin
@command(MentionSchema)
async def process_inspect(client, message, mention):
    user = db.session.query(User).filter_by(id=mention).first()
    if not user:
        await client.send_message(message.channel, 'I can\'t find that user')
        return

    resp = '```id: {}\n\nInventory:'.format(user.id)
    for item in user.items:
        resp += '\n{} x{} id: {}'.format(item.name, item.quantity, item.id)
    resp += '```'
    await client.send_message(message.channel, resp)


@requires_admin
@command(NumericSchema)
async def process_delete(client, message, number):
    item = db.session.query(Item).filter_by(id=number).first()
    if not item:
        await client.send_message(message.channel, 'I can\'t find that item')
        return

    item.delete()
    await client.send_message(message.channel, '{} removed'.format(item.name))


@requires_admin
@command(GrantSchema)
async def process_grant(client, message, mention, name, quantity):
    user = db.session.query(User).filter_by(id=mention).first()
    if not user:
        await client.send_message(message.channel, 'I can\'t find that user')
        return

    add_item(user, name, quantity)
    await client.send_message(message.channel, 'Granted {} {}'.format(quantity, name))


@requires_admin
@command(GrantSchema)
async def process_remove(client, message, mention, name, quantity):
    user = db.session.query(User).filter_by(id=mention).first()
    if not user:
        await client.send_message(message.channel, 'I can\'t find that user')
        return

    add_item(user, name, -quantity)
    await client.send_message(message.channel, 'Removed {} {} from {}'.format(quantity, name, user.mention))


@requires_admin
@command(MentionSchema)
async def process_force_abandon(client, message, mention):
    user = db.session.query(User).filter_by(id=mention).first()
    if not user:
        await client.send_message(message.channel, 'I can\'t find that user')
        return

    user.update(is_exploring=False, ticks=0, initial_ticks=0)
    await client.send_message(message.channel, 'Kicked {} out of their exploration'.format(user.mention))