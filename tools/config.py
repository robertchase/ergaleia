'''
The MIT License (MIT)

https://github.com/robertchase/tools/blob/master/LICENSE.txt
'''
import os

from tools.load_from_path import load_lines_from_path
import tools.string_util as string_util


class Config (object):

    '''
      Class to manage 'key.name=value' style configuration records.

      A Config is first initialized, by passing the definition parameter to the
      constructor, or by calling _define or _define_from_file methods.
      The initialization step specifies each valid configuration type by
      supplying a name, which is a sequence of dot (.) delimited tokens, along
      with an optional initial value and optional validation function.

      User supplied configuration values, perhaps from a configuration file (see
      _load), are specified to the _set method, which accepts a name and a
      value. The name must match a name specified with the _define method, and
      the value will be run through the validation function specified with the
      _define method.

      The config object will yield values for defined names using a standard
      python object syntax. So, if a configuration item is defined with the
      name 'server.address', and the configuration object is assigned to
      the variable 'cfg', then the 'server.address' value is accessed with this
      syntax:

        cfg.server.address

      as though it were a hierachy of python objects.

      NOTES:

      1. Methods are prepended with '_' in order not to pollute the namespace
         used by the defined values.

      2. Valid names are composed of letters, digits, underscores and periods.
         No part of a valid name can be composed only of digits.

      3. The _load function ignores leading and trailing whitespace in the
         names and values.

      4. The _load function ignores anything including and following a '#'
         character, thus allowing for comments. To prevent a '#' value from
         starting a comment, escape it by preceeding it with a '\' character.

      5. If the env parameter is specified on the _define function, and an
         env variable of this name is set, then the value of the env variable
         overrides the 'value' parameter and any parmemter read from the config
         file.

    '''

    def __init__(self, definition=None):
        self.ordered_keys = []
        self._values = ConfigItem()
        self._direct = {}
        if definition:
            self._define_from_file(definition)

    def __repr__(self):
        return '\n'.join(
            '%s=%s' % (
                k, getattr(self, k)
                if getattr(self, k)
                is not None else ''
            )
            for k in self.ordered_keys
        )

    def __getattr__(self, name):
        if '.' in name:
            return self._get(name)
        return getattr(self._values, name)

    def _get(self, name):
        parts = name.split('.')
        item = getattr(self, parts[0])
        for part in parts[1:]:
            item = getattr(item, part)
        return item

    def _define(self, name, value=None, validator=None, env=None):
        if name not in self.ordered_keys:
            self.ordered_keys.append(name)
        item = self._values
        for part in name.split('.'):
            if not isinstance(item._value, dict):
                raise AttributeError(
                    "Leaf node cannot be extended with '%s'" % part)
            if part not in item._value:
                item._value[part] = ConfigItem()
            item = item._value[part]
        if isinstance(item._value, dict) and len(item._value):
            raise AttributeError(
                "Non-leaf node '%s' cannot be assigned" % part)
        item._validator = validator
        item._env = os.getenv(env) if env else None
        if item._env and validator:
            item._env = validator(item._env)
        if value and validator:
            value = validator(value)
        item._value = value
        self._direct[name] = item

    def _define_from_file(self, path):
        data = load_lines_from_path(path)
        for num, line in enumerate(data, start=1):
            try:
                args, kwargs = string_util.to_args(line)
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

    def _set(self, name, value):
        if name not in self._direct:
            raise AttributeError(
                "'%s' is not a defined config parameter" % name
            )
        item = self._direct[name]
        if item._validator:
            value = item._validator(value)
        item._value = value

    def _load(self, config):
        '''
            Load values into an already defined Config.

            Parameters:
                config - a str filename, a list, or a file-like object (that
                         supports readlines)

            Records (lines) are read from the config parameter and parsed as

                <name>=<value>

            where <name> matches a name specified in an earlier _define
            call and <value> is the new value associated with that name.
        '''

        if isinstance(config, str):
            if not os.path.exists(config):
                return
            config = open(config).readlines()
        elif isinstance(config, list):
            pass
        else:
            config = config.readlines()

        for lineno, line in enumerate(config, start=1):

            line = string_util.un_comment(line)
            if len(line) == 0:
                continue

            try:
                key, value = line.split('=', 1)
                self._set(key.strip(), value.strip())
            except ValueError:
                raise ValueError(
                    'Error on line {} of config: invalid syntax'.format(lineno)
                )
            except Exception as e:
                raise Exception(
                    'Error on line {} of config: {}'.format(lineno, e)
                )


class ConfigItem (object):

    def __init__(self, name=None):
        self._value = {}
        self._validator = None
        self._counter = None
        self._default = None

    def __getattr__(self, name):
        if name in self._value:
            item = self._value[name]
            if item._counter or isinstance(item._value, dict):
                return item
            return item._env if item._env is not None else item._value
        raise AttributeError("'%s' not found" % name)

    def __getitem__(self, key):
        key = str(key)
        if self._default:
            return self._value.setdefault(key, self._default)
        return self._value[key]


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
