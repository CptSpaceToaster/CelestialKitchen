import itertools
import functools

from celestialKitchen.database import db
from celestialKitchen.models.user import User
from celestialKitchen.models.area import Area


class ValidatorException(Exception):
    def __init__(self, reason):
        self.reason = reason


class Validator(object):
    def __init__(self, name, default=None):
        self.name = name
        self.default = default

    def validate(self, token):
        return token


class ValidatorsExhausted(Exception):
    pass


class MissingRequiredArgument(Exception):
    def __init__(self, name):
        self.name = 'Missing required argument: ' + name


class Schema(object):
    def __init__(self, validators=[]):
        self.validators = validators

    def validate(self, tokens):
        kwargs = {}
        for token, validator in itertools.zip_longest(tokens, self.validators):
            if token and validator:
                kwargs[validator.name] = validator.validate(token)
            elif validator:
                if validator.default is not None:
                    kwargs[validator.name] = validator.default
                else:
                    raise MissingRequiredArgument(validator.name)
            else:
                raise ValidatorsExhausted
        return kwargs


async def handle_validator_exception(client, message, text):
    await client.send_message(message.channel, text)


def command(schema):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            tokens = kwargs.pop('tokens')
            if schema:
                try:
                    new_kwargs = {**kwargs, **schema.validate(tokens)}
                    return await func(*args, **new_kwargs)
                except ValidatorException as e:
                    return await handle_validator_exception(*args, e.reason, **kwargs)
                except ValidatorsExhausted:
                    return await handle_validator_exception(*args, 'Sorry, I don\'t understand what you\'re trying to say', **kwargs)
                except MissingRequiredArgument as e:
                    return await handle_validator_exception(*args, e.name, **kwargs)
        return wrapper
    return decorator


class BooleanValidator(Validator):
    def validate(self, token):
        if len(token) == 0 or token.lower() == 'false' or token.lower() == 'f':
            return False
        else:
            return True


class IdValidator(Validator):
    def validate(self, token):
        if not token.startswith('<@') or not token.endswith('>'):
            raise ValidatorException('User wasn\'t properly mentioned')
        token = token.lstrip('<@')
        token = token.lstrip('!')
        token = token.rstrip('>')
        if not token.isnumeric():
            raise ValidatorException('User mention wasn\'t numeric')
        return token


class MentionValidator(IdValidator):
    def validate(self, token):
        token = IdValidator.validate(self, token)
        user = db.session.query(User).filter_by(id=token).first()
        if not user:
            raise ValidatorException('I can\'t find that user')
        return user


class NumericValidator(Validator):
    def validate(self, token):
        if not token.isnumeric():
            raise ValidatorException('Please enter a number.')
        return int(token)


class AreaValidator(Validator):
    def validate(self, token):
        area = db.session.query(Area).filter(Area.name.ilike(token)).first()
        if not area:
            raise ValidatorException('I can\'t find an area named: {}'.format(token))
        return area


class RecipeValidator(Validator):
    def validate(self, token):
        # recipe = recipes.get(token, None)
        # if not recipe:
        #     raise ValidatorException('I don\'t know what a {} is'.format(token))
        # return recipe
        return token


EmptySchema = Schema()
IdSchema = Schema(validators=[MentionValidator('id')])
MentionSchema = Schema(validators=[MentionValidator('user')])
NumericSchema = Schema(validators=[NumericValidator('number')])
GrantSchema = Schema(validators=[MentionValidator('user'), Validator('name'), NumericValidator('quantity', default=1)])
ExploreSchema = Schema(validators=[AreaValidator('recipe')])
CraftSchema = Schema(validators=[RecipeValidator('recipe')])
NameSchema = Schema(validators=[Validator('name')])
AreaSchema = Schema(validators=[AreaValidator('area')])
DropsSchema = Schema(validators=[AreaValidator('area'), BooleanValidator('show_command', default=False)])
NewDropSchema = Schema(validators=[AreaValidator('area'), Validator('name'), NumericValidator('quantity'), NumericValidator('ticks'), NumericValidator('weight', default=1)])
RemoveDropSchema = Schema(validators=[AreaValidator('area'), Validator('name')])
AdjustDropSchema = Schema(validators=[AreaValidator('area'), Validator('name'), NumericValidator('number')])
