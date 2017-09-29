from flask import g


def g_get(key, creator):
    """Returns an instance that is cached on the flask global `g` object.

    If the `key` is accessed for the first time, `creator` is expected to
    return the instance in question.
    """
    if not hasattr(g, key):
        setattr(g, key, creator())
    return getattr(g, key)


def g_factory(key, creator):
    """Returns a factory method that returns an instance that is bound
    to the flask global object `g`."""
    def factory():
        return g_get(key, creator)
    return factory
