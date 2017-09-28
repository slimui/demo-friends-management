from flask import request, g
from .models import User
from .logging import logger


CURRENT_USER_ID_KEY = 'x-app-current-user-id'


def current_user_id():
    """Returns the current user_id that is 'logged in'.
    Typically this information is saved in the session cookie upon successful
    user authentication. For the demo we allow users to 'switch' identity
    by providing a 'x-app-current-user-id' information.

    When this information is not available, e.g. during testing, the default
    user_id = 1 is used.

    This method must be used within a flask request context."""
    if not hasattr(g, 'current_user_id'):
        try:
            id = int(request.headers.get(CURRENT_USER_ID_KEY))
        except:
            id = 1
        if not id:
            id = 1
        setattr(g, 'current_user_id', id)
    return g.current_user_id


def current_user():
    """Returns the `User` instance of the `current_user_id` identity.

    This method must be used within a flask request context."""
    if not hasattr(g, 'current_user'):
        try:
            user = User.query.get(current_user_id())
        except Exception as e:
            logger.exception(e)
            user = None
        setattr(g, 'current_user', user)
    return g.current_user
