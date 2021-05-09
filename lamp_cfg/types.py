from .exceptions import UndefinedField


def keep_type(value):
    """
    Keep hook returned value type

    :param value: Value to be returned
    :return: Any
    """

    return value


class Field:
    def __init__(self, name, type_=str,
                 optional=False, validator=None,
                 local_alias=None, default_value=None,
                 parse_hook=lambda x: x):
        """
        :param type_: Type of the field
        :type type_: callable

        :param name: Name of the field
        :type name: str

        :param optional: Optionality of this parameter
        :type optional: bool

        :param validator: Validator
        :type validator: callable

        :param local_alias: Alias that will be used in Lamp factory
        :type local_alias: str

        :param default_value: Default value for this field
        """

        self.name = name
        self.type = type_
        self.optional = optional
        self.validator = validator
        self.local_alias = local_alias
        self.default_value = default_value
        self.parse_hook = parse_hook

    def __repr__(self):
        return "<Field name=%r type=%s>" % (self.name, self.type)

    __str__ = __repr__

    def __eq__(self, other):
        if isinstance(other, Field):
            return other.name == self.name

        return other == self.name


class Namespace:
    """
    Config namespace
    """

    def __init__(self, ns_name, fields):
        """
        :param ns_name: Namespace name
        :type ns_name: str

        :param fields: Fields
        :type fields: list
        """

        self.ns_name = ns_name
        self.fields = fields

    def by_name(self, name,
                lineno=-1):
        """
        Get field by the name

        :param name: Name of field
        :type name: str

        :param lineno: Optional parameter for config parser
        :type lineno: int

        :return: Field
        """

        if name not in self.fields:
            raise UndefinedField("Undefined field %r on line %d" % (name, lineno))

        for field in self.fields:
            if field == name:
                return field

    def __eq__(self, other):
        """
        Checks if other is equals to self by name

        :param other: namespace or string
        :return: bool
        """

        if isinstance(other, Namespace):
            return other.ns_name == self.ns_name

        return self.ns_name == self.ns_name

    @classmethod
    def merge(cls, ns1, ns2,
              ns_name=None):
        """
        Merges two namespaces, uses name of first or custom

        :param ns_name: New namespace name
        :type ns_name: str

        :param ns1: First namespace
        :type ns1: Namespace

        :param ns2: Second namespace
        :type ns2: Namespace

        :return: Namespace
        """

        fields = [*ns1.fields, *ns2.fields]
        namespace = cls(ns1.ns_name or ns_name, fields)

        return namespace
