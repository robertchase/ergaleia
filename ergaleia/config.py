from collections import namedtuple
import os

from ergaleia.import_by_path import import_by_path
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

    def __init__(self, definition=None, filetype=None):
        self.__dict__['_ordered_keys'] = []
        if definition:
            self._define_from_path(definition, filetype)

    def __repr__(self):
        return '\n'.join(
            '{}={}'.format(
                k, v if v is not None else ''
            ) for k, v in self.__ordered()
        )

    def __ordered(self):
        return [(k, self._get(k)) for k in self.__dict__['_ordered_keys']]

    def __lookup(self, name):
        level = self
        parts = str(name).split('.')
        parts, itemname = parts[:-1], parts[-1]
        for part in parts:
            level = level[part]
        return level, itemname

    def _define(self, name, value=None, validator=None, env=None):
        keys = self.__dict__['_ordered_keys']
        if name not in keys:
            keys.append(name)
        parts = str(name).split('.')
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

    def _define_from_path(self, path, filetype=None):
        data = un_comment(load_lines_from_path(path, filetype))
        for num, line in enumerate(data, start=1):
            if not line:
                continue
            try:
                args, kwargs = to_args(line)
                if 'validator' in kwargs:
                    validator = kwargs.get('validator')
                    try:
                        kwargs['validator'] = _VALIDATE_MAP[validator]
                    except KeyError:
                        try:
                            kwargs['validator'] = import_by_path(validator)
                        except Exception:
                            raise Exception(
                                'Invalid validator: {}'.format(validator)
                            )
                self._define(*args, **kwargs)
            except Exception as e:
                raise Exception(
                    'Error on line {} of definition: {}'.format(num, e)
                )

    def _load(self, path='config', filetype=None, relaxed=False, ignore=False):
        """ load key value pairs from a file

            Parameters:
                path     - path to configuration data (see Note 1)
                filetype - type component of dot-delimited path
                relaxed  - if True, define keys on the fly (see Note 2)
                ignore   - if True, ignore undefined keys in path

            Return:
                self

            Notes:

                1. The path can be:
                    * an open file object with a readlines method
                    * a dot delimited path to a file (see normalize_path)
                    * an os-specific path to a file (relative to cwd)
                    * an iterable of key=value strings

                2. Normally keys read from the file must conform to keys
                   previously defined for the Config. If the relaxed flag
                   is True, any keys found in the file will be accepted.
                   If the ignore flag is True, and kyes found in the file
                   that are not previously defined are ignored.
        """
        for num, line in enumerate(
                    un_comment(load_lines_from_path(path, filetype)),
                    start=1,
                ):
            if not line:
                continue
            try:
                key, val = line.split('=', 1)
                key = key.strip()
                val = val.strip()
                if relaxed:
                    self._define(key)
                try:
                    level, itemname = self.__lookup(key)
                except KeyError:
                    if ignore:
                        continue
                    raise
                item = level.get(itemname)
                if item is None:
                    raise KeyError(itemname)
                item.load(val)
            except Exception as e:
                args = e.args or ('',)
                msg = 'line {} of config: {}'. format(num, args[0])
                e.args = (msg,) + args[1:]
                raise
        return self

    @property
    def _as_dict(self):
        return {k: v for k, v in self.__ordered()}

    def _get(self, name):
        level, itemname = self.__lookup(name)
        try:
            return level[itemname]
        except TypeError:
            raise KeyError(itemname)

    def _set(self, name, value):
        level, itemname = self.__lookup(name)
        level[itemname] = value


class _item(object):

    def __init__(self, value, validator, env):
        self.reset(value, validator, env)

    def __setattr__(self, name, value):
        """ directly setting value does not respect env """
        validator = self.validator
        if value and validator:
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
    'int': int,
    'bool': validate_bool,
    'file': validate_file,
}


class Mini(object):
    """ limited one-level config

        Define field names (no dots) with string arguments to the constructor.

        Set values in the normal way, or using kwargs to the set method.

        Load values from a file with the load method.

        Return a namedtuple of key-values with the as_tuple method.
    """

    def __init__(self, *args):
        self.__dict__['conf'] = Config(args)

    def __getattr__(self, name):
        return self.conf[name]

    def __setattr__(self, name, value):
        self.__dict__['conf'][name] = value

    def set(self, **kwargs):
        for k, v in kwargs.items():
            self.__dict__['conf'][k] = v

    def load(self, path):
        self.conf._load(path)

    def as_tuple(self, name='MiniConfig'):
        return namedtuple(name, self.conf._ordered_keys)(
            **{n: self.conf._get(n) for n in self.conf._ordered_keys}
        )


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='parse a config file',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        '-c', '--config',
        type=argparse.FileType('r'),
        help='configuration file'
    )
    parser.add_argument(
        '-d', '--defn',
        type=argparse.FileType('r'),
        help='config definition file'
    )
    parser.add_argument(
        '-r', '--relaxed', default=False, action='store_true',
        help='accept all keys found in config file (define on the fly)'
    )
    args = parser.parse_args()

    c = Config(args.defn)
    if args.config:
        c._load(args.config, relaxed=args.relaxed)
    print(c)
