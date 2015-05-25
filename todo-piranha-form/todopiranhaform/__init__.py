from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.session import UnencryptedCookieSessionFactoryConfig
from .usersdb import groupfinder


from .models import (
    DBSession,
    Base,
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    my_session_factory = UnencryptedCookieSessionFactoryConfig('itsaseekreet')
    # TODO: move mysecret to conf file
    authn_policy = AuthTktAuthenticationPolicy(
        'mysecret', callback=groupfinder, hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()

    config = Configurator(
        settings=settings,
        root_factory='todopiranhaform.rootfactory.RootFactory',
        session_factory=my_session_factory,
    )
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)

    config.include('pyramid_chameleon')
    config.include('pyramid_jinja2')

    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_static_view('deform_static', 'deform:static')
    config.add_route('home', '/')
    config.add_route('viewform', '/viewform')
    config.add_route('todofiltered', '/todo/{viewtype}')
    config.add_route('viewtodo', '/todo')
    config.add_route('clear_completed', '/clear_completed')
    config.add_route('task_delete', '/task_delete/{taskid}')
    config.add_route('task_complete', '/task_complete/{taskid}')
    config.add_route('todo_json', '/todo_json')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.scan()
    return config.make_wsgi_app()
