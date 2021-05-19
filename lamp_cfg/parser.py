from .types import Namespace, Field
from .exceptions import (UndefinedNamespace, ValidatorError,
                         NoNamespace, UndefinedField)


def _get_namespace_name(text, lineno):
    if not text.endswith(']'):
        raise SyntaxError("Namespace definition out of line(line %d)" % lineno)

    return text[1:-1]


def _remove_comments(text):
    if '#' not in text:
        return text

    return text[:text.find('#')].strip()


def _parse_param(line, assignment_pos):
    key = line[:assignment_pos].strip()
    value = line[assignment_pos+1:].strip()

    return key, value


def _validate_namespace(settings, namespace_name,
                        lineno):
    if namespace_name not in settings:
        raise UndefinedNamespace("Undefined namespace name %r on line %d" % (namespace_name, lineno))


def _validate_value(field, value,
                    lineno):
    """
    Validates the given value
    :param field: settings for the field
    :type field: Field

    :param lineno: Line number
    :type lineno: int

    :param value: Value to be validated
    :return:
    """


def _get_ns_by_name(namespaces, name,
                    lineno):
    if name is None:
        raise NoNamespace("No namespace for parameter definition on line %d" % lineno)

    for namespace in namespaces:
        if namespace.ns_name == name:
            return namespace


def _post_validate_ns(namespace, setting):
    """
    :param namespace:
    :type namespace: dict

    :param setting:
    :type setting: Namespace

    :return:
    """

    for field in setting.fields:
        if field.name not in namespace:
            if not field.optional:
                raise UndefinedField("Undefined field %r" % field.name)

            namespace[field.name] = field.default_value


def parse_cfg(text, settings,
              constants=None):
    if constants is None:
        constants = {}

    """
    :param settings: A List of Namespaces
    :param text: Text version of config
    :param constants: Constants used in config
    
    :return: dict
    """

    current_namespace = None
    namespaces = {}
    lines = text.splitlines()

    for lineno, line in enumerate(lines):
        line = _remove_comments(line.strip())

        if not line:
            continue

        if line.startswith('['):  # namespace definition
            name = _get_namespace_name(line, lineno)

            _validate_namespace(settings, name,
                                lineno)

            current_namespace = name
            namespaces[name] = {}

            continue

        assignment_pos = line.find('=')

        if assignment_pos == -1:
            raise SyntaxError("Unknown expression passed on line %d" % lineno)

        key, value = _parse_param(line, assignment_pos)
        namespace = _get_ns_by_name(settings, current_namespace,
                                    lineno)
        field = namespace.by_name(key)

        if value.startswith('%'):
            value = constants[value[1:]]

        value = field.parse_hook(value)

        if field.validator:
            validation_value = field.validator(value)

            if not validation_value:
                raise ValidatorError("Failed validation")

        namespaces[current_namespace][key] = field.type(value)

    for namespace in settings:
        if namespace.ns_name in namespaces:
            _post_validate_ns(namespaces[namespace.ns_name], namespace)

    return namespaces


def from_file(filename, settings,
              constants=None):
    """
    :param filename: File name
    :type filename: str

    :param constants: Constants used in config
    :type constants: dict

    :param settings: A List of Namespaces
    :return: dict
    """

    with open(filename, 'r', encoding='utf-8') as file:
        return parse_cfg(file.read(), settings,
                         constants)
