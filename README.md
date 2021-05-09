# lamp_cfg
Configuration files parser

# Config format
Config has an ini-like format.

`[name]` - namespace definition

`key=value` - config value definition(attached to namespace)


example:
```text
[Server]
listen_port=6567 # listening port
listen_addr=0.0.0.0 # listening host, 0.0.0.0 - any address
```


# Definition config fields and namespaces

```python
from lamp_cfg.types import Namespace, Field

# Field - config field attached to namespace
# Namespace - config namespace, that contains attached fields

settings = Namespace(
    'Server', (
        Field('listen_port', int,
              False, lambda port: port <= 65535),
        Field('listen_addr', str, 
              False)
    )
)
```

Config fields definition are just like namedtuple creation, classes signature:

## Field

```python
Field(name, type_=str,
      optional=False, validator=None,
      local_alias=None, default_value=None,
      parse_hook=lambda x: x)
```

parse_hook - Pre-parse hook for value, by default always returning the given value

optional - optionality of the field

default_value - default value of the field if not noted

local_alias - TODO: add usability for this field, alternative name of the field

validator - field validator function, passed argument is already parsed

type_ - type of value, used to parse value by calling its constructor, if you want to keep value as it returned by parse_hook, then pass `lamp_cfg.types.keep_type`

## Namespace

```python
Namespace(name, fields)
```

name - name of namespace

fields - list of fields


# Parsing defined config


```python
from lamp_cfg.parser import parse_cfg, from_file

# from_file - parse config from file
# parse_cfg - parse config from text

# %name - constant passed to parse function

text_cfg = parse_cfg("[test]\nok=%OK_VALUE", [
    # list of namespaces
], constants={
    'OK_VALUE': 1
})

file_cfg = from_file('lamp.lcfg', [
    # list of namespaces
], constants={
    'OK_VALUE': 1
})


```

