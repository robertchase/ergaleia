import os

from ergaleia.load_from_path import load_lines_from_path
from ergaleia.to_args import to_args
from ergaleia.un_comment import un_comment


class _branch(dict):

    def __lookup(self, name):
        if name not in self:
            raise KeyError(name)
        return self.get(name)

    def __getattr__(self, name):
        attr = self.__lookup(name)
        if isinstance(attr, _item):
            return attr.value
        return attr

    def __getitem__(self, name):
        return self.__getattr__(name)

    def __setattr__(self, name, value):
        attr = self.__lookup(name)
        if not isinstance(attr, _item):
            raise AttributeError(name)
        attr.value = value

    def __setitem__(self, name, value):
        self.__setattr__(name, value)


class Config(_branch):
    """ Manage 'key=value' style configuration records.

        A Config is a constrained-key nested-dict whose values can be acccessed
        using bracket or dot notation. Typically, the expected keys are defined
        during setup, and the values are read from a configuration file.

        Use a series of calls to the _define method to establish a valid
        structure. Key names can contain dots (.) which act to separate the
        name space and mitigate access to the Config data structure. For
        instance:

            c = Config()
            c._define('server.port', value=1234)

            # access the new key
            assert c.server.port == 1234

            # bracket notation works too
            assert c['server']['port'] == 1234

        Use the _load method to read and parse the values in a config file.
        Only defined keys will be accepted. To change the default value in the
        previous example, the config file might look like this:

            server.port=2345

      Notes:

      1. Methods are prepended with '_' in order not to pollute the namespace
         used by the defined values.

      2. Valid names are composed of letters, digits, underscores and periods.
         No part of a valid name can be composed only of digits.

      3. The _load method ignores leading and trailing whitespace in the
         names and values.

      4. The _load method ignores anything including and following a '#'
         character, thus allowing for comments. To prevent a '#' value from
         starting a comment, escape it by preceeding it with a '\' character.

      5. If the env parameter is specified on the _define function, and an
         env variable of this name is set, then the value of the env variable
         overrides the 'value' parameter and any parmemter read using the _load
         method. Values which are directly set override env.
    """

    def __init__(self, definition=None):
        self.__dict__['_ordered_keys'] = []
        if definition:
            self._define_from_file(definition)

    def __repr__(self):
        return '\n'.join(
            '{}={}'.format(
                k, getattr(self, k) if getattr(self, k) is not None else ''
            ) for k in self.__dict__['_ordered_keys']
        )

    def __lookup(self, name):
        level = self
        parts = name.split('.')
        parts, itemname = parts[:-1], parts[-1]
        for part in parts:
            level = level[part]
        return level, itemname

    def _define(self, name, value=None, validator=None, env=None):
        keys = self.__dict__['_ordered_keys']
        if name not in keys:
            keys.append(name)
        parts = name.split('.')
        parts, itemname = parts[:-1], parts[-1]
        level = self
        for part in parts:
            level = level.setdefault(part, _branch())
            if isinstance(level, _item):
                raise Exception(
                    'member {} of {} is a leaf node'.format(part, name)
                )
        item = level.get(itemname)
        if item:
            if isinstance(item, _item):
                item.reset(value, validator, env)
            else:
                raise Exception(
                    'member {} of {} is a branch node'.format(itemname, name)
                )
        else:
            level.setdefault(itemname, _item(value, validator, env))

    def _define_from_file(self, path):
        data = load_lines_from_path(path)
        for num, line in enumerate(data, start=1):
            try:
                args, kwargs = to_args(line)
                if 'validator' in kwargs:
                    validator = kwargs.get('validator')
                    try:
                        kwargs['validator'] = _VALIDATE_MAP[validator]
                    except KeyError:
                        raise Exception(
                            'Invalid validator: {}'.format(validator)
                        )
                self._define(*args, **kwargs)
            except Exception as e:
                raise Exception(
                    'Error on line {} of definition: {}'.format(num, e)
                )

    def _load(self, path='config', relaxed=False):
        for line in load_lines_from_path(path):
            line = un_comment(line)
            if not line:
                continue
            key, val = line.split('=', 1)
            key = key.strip()
            val = val.strip()
            if relaxed:
                self._define(key)
            level, itemname = self.__lookup(key)
            level.get(itemname).load(val)

    def _get(self, name):
        level, itemname = self.__lookup(name)
        return level[itemname]

    def _set(self, name, value):
        level, itemname = self.__lookup(name)
        level[itemname] = value


class _item(object):

    def __init__(self, value, validator, env):
        self.reset(value, validator, env)

    def __setattr__(self, name, value):
        """ directly setting value does not respect env """
        validator = self.validator
        if validator:
            value = validator(value)
        self.__dict__['value'] = value

    def reset(self, value, validator, env):
        self.__dict__['validator'] = validator
        self.__dict__['env'] = env
        if env:
            value = os.getenv(env, value)
        self.value = value

    def load(self, value):
        """ enforce env > value when loading from file """
        self.reset(
            value,
            validator=self.__dict__.get('validator'),
            env=self.__dict__.get('env'),
        )


def validate_int(value):
    return int(value)


def validate_bool(value):
    if value in (0, 1):
        return (False, True)[value]
    if value in (True, False):
        return value
    try:
        return {'TRUE': True, 'FALSE': False}[value.upper()]
    except AttributeError:
        raise ValueError
    except KeyError:
        raise ValueError


def validate_file(value):
    if len(value) == 0:
        return value
    if os.path.isfile(value):
        return value
    raise Exception("file '%s' not found" % value)


_VALIDATE_MAP = {
    'int': validate_int,
    'bool': validate_bool,
    'file': validate_file,
}
