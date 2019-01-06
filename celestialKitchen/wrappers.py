import functools
import discord

from celestialKitchen.config import config
from celestialKitchen.client import client
from celestialKitchen.database import db
from celestialKitchen.models.server import Server
from celestialKitchen.models.user import User, register_new_user


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
                user = register_new_user(id=author.id, name=author.name, display_name=author.display_name, mention=author.mention, destination=message.channel.id)
            else:
                user.update(name=author.name, display_name=author.display_name, mention=author.mention, destination=message.channel.id)
        kwargs['user'] = user
        return await func(*args, **kwargs)
    return wrapper


def fetch_server(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        message = args[1]
        server = None
        if isinstance(message, discord.Message) and message.server.id:
            server = db.session.query(Server).filter_by(id=message.server.id).first()
        kwargs['server'] = server
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
            return await client.send_message(message.channel, 'You don\'t have admin permissions to use that command')
    return wrapper


def requires_mod(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        message = args[1]
        if isinstance(message, discord.Message) and message.server.id:
            server = db.session.query(Server).filter_by(id=message.server.id).first()
            for mod in server.mods:
                if message.author.id == mod.id:
                    return await func(*args, **kwargs)
        return await client.send_message(message.channel, 'You don\'t have mod permissions to use that command')
    return wrapper
