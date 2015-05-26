import os
import sys
import transaction

from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from ..models import (
    DBSession,
    Task,
    User,
    Base,
    )


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    with transaction.manager:
        model = Task(taskname='Learn 101 of telekinesis', status=False)
        DBSession.add(model)
        model = Task(taskname='Bend 20 forks', status=True)
        DBSession.add(model)
        model = Task(taskname='Become master in levitation', status=True)
        DBSession.add(model)
        model = Task(taskname='Go home flying', status=True)
        DBSession.add(model)

    with transaction.manager:
        admin = User(name=u'admin', password=u'admin')
        DBSession.add(admin)
        admin = User(name=u'demo', password=u'demo')
        DBSession.add(admin)
