import sys
import asyncio
import discord
import pkgutil
import importlib

from celestialKitchen.database import db
from celestialKitchen.config import config
from celestialKitchen.tasks import do_explore
from celestialKitchen.models.server import Server
from celestialKitchen.models.user import User

client = discord.Client()
command_prefix = config.DEFAULT_COMMAND_PREFIX
command_modules = [name for _, name, _ in pkgutil.iter_modules(['celestialKitchen/commands'], 'celestialKitchen.commands.')]

print(command_modules)
print(__name__)

for c in command_modules:
    importlib.import_module(c)


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
    print('Registered {} recipes'.format('TODO'))


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

    func = None
    for module_name in command_modules:
        try:
            func = getattr(sys.modules[module_name], function_name)
            if func:
                break
        except AttributeError:
            pass  # continue?
    if func:
        try:
            if config.ENV == 'dev':
                print(function_name, parsed_tokens)
            await func(client, message, tokens=parsed_tokens)
        except Exception as e:
            print('Problem in handler {} - {}'.format(function_name, message.content))
            raise e
