from sqlalchemy import event as sa_event

from mapping_extend import mapping_extend


class SerializableModel(object):
    """Base model class for a model that will self-serialize to JSON"""

    __json_args__ = None

    @classmethod
    def init_json_args(cls):
        """Initialize the __json_args__ to sane defaults. If __json_args__ is specified on this class, it's values will
        extend the defaults.
        The default output configuration does not include any relationships."""
        defaults = cls._base_json_args()

        if cls.__json_args__ is None:
            cls.__json_args__ = defaults
        else:
            cls.__json_args__ = mapping_extend(defaults, cls.__json_args__)

    @classmethod
    def _base_json_args(cls):
        """Return the baseline json args for this model, with no relationships being included"""
        relationships = cls.__mapper__.relationships.keys()
        relationship_options = dict([(x, False) for x in relationships])

        defaults = {'relationships': relationship_options,
                    'exclude_attrs': [],
                    'include_attrs': []}
        return defaults

    def __json__(self, request, options={}):
        """Serialize a model object to a JSON-compatible dict.
        Relationships are included or not based on their boolean value in `self.__json_args__['relationships']`.
        If an attribute is specified in __json_args__['exclude_attrs'], it will be excluded UNLESS it is also
        included (therefore overridden) in __json_args__['include_attrs'].
        If the '_overridden' key is present, instead of extending the base __json_args__ for the class, the provided
        options dict will extend the base json args, instead of the one defined on this class."""
        if '_override' not in options:
            json_args = mapping_extend({}, self.__json_args__, options)
        else:
            # Full override
            json_args = mapping_extend({}, self._base_json_args(), options)
        obj = {}
        for column in self.__table__.columns:
            if '*' not in json_args['exclude_attrs'] and column.name not in json_args['exclude_attrs'] or \
                (column.name in json_args['include_attrs']):
                    obj[column.name] = getattr(self, column.name)

        for relationship_name in [name for (name, include) in json_args['relationships'].items() if include is True]:
            try:
                relationship = self.__mapper__.relationships[relationship_name]
            except KeyError:
                # Relationship does not exist on this instance, was probably
                # specified for another object type in a recursive serialization
                continue
            if relationship.uselist:
                obj[relationship_name] = [instance.__json__(request, options) for instance in getattr(self, relationship_name)]
            else:
                relationship_value = getattr(self, relationship_name)
                if relationship_value is not None:
                    relationship_value = relationship_value.__json__(request, options)
                obj[relationship_name] = relationship_value

        return obj

def mapper_configured_listener(mapper, cls):
    cls.init_json_args()
sa_event.listen(SerializableModel, 'mapper_configured', mapper_configured_listener, propagate=True)
