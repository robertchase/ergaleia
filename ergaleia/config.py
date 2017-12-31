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

    def __init__(self, definition=None):
        if definition:
            self._define_from_file(definition)

    def __lookup(self, name):
        level = self
        parts = name.split('.')
        parts, itemname = parts[:-1], parts[-1]
        for part in parts:
            level = level[part]
        return level, itemname

    def _define(self, name, value=None, validator=None, env=None):
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
            if relaxed:
                self._define(key)
            self._set(key.strip(), val.strip())

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
        validator = self.validator
        if validator:
            value = validator(value)
        self.__dict__['value'] = value

    def reset(self, value, validator, env):
        self.__dict__['validator'] = validator
        if env:
            value = os.getenv(env, value)
        self.value = value


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
