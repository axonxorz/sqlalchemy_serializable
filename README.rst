sqlalchemy_serializable
===================

Base class for SQLAlchemy models to implement the Pyramid __json__ protocol.
A base __json__ method is provided for all model classes, it can be overridden fully,
or have basic behaviour changed with a __json_args__ dict or callable.

