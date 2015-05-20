from pyramid.security import Allow
from pyramid.security import Authenticated
# from pyramid.security import Everyone


class RootFactory(object):
    """This object sets the security for our application. In this case
    we are only setting the `view` permission for all authenticated
    users.
    """
    # __acl__ = [(Allow, Everyone, 'view')]
    __acl__ = [
        (Allow, Authenticated, 'view'),
        # (Allow, 'group:admin', 'edit'),
        # DENY_ALL
    ]

    def __init__(self, request):
        pass
