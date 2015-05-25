import unittest
import transaction

from pyramid.paster import get_app

from pyramid import testing

from .models import DBSession


class TestMyViewSuccessCondition(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        from sqlalchemy import create_engine
        engine = create_engine('sqlite://')
        from .models import (
            Base,
            TaskModel,
            )
        DBSession.configure(bind=engine)
        Base.metadata.create_all(engine)
        with transaction.manager:
            model = TaskModel(taskname='one', status=True)
            DBSession.add(model)

    def tearDown(self):
        DBSession.remove()
        testing.tearDown()

    def test_passing_view(self):
        from .views import todo_json
        request = testing.DummyRequest()
        tasklist = todo_json(request)
        self.assertEqual(tasklist[0]['taskid'], '1')
        self.assertEqual(tasklist[0]['description'], 'Learn 101 of telekinesis')


class TutorialViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    # def test_todofiltered(self):
    #     from .views import viewtodo

    #     request = testing.DummyRequest()
    #     request.matchdict = {'viewtype': 'COMPLETED'}
    #     response = viewtodo(request)
    #     self.assertEqual(response.status_code, 200)

    def test_todo_json(self):
        from .views import todo_json
        request = testing.DummyRequest()
        response = todo_json(request)
        self.assertEqual(len(response), 4)


class TutorialAuthentication(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    # def test_view_todo(self):
    #     from .views import viewtodo
    #     request = testing.DummyRequest()
    #     response = viewtodo(request)
    #     self.assertEqual(len(response), 4)

    # def test_view_todo_forbidden(self):
    #     from pyramid.httpexceptions import HTTPForbidden
    #     from .views import viewtodo
    #     self.config.testing_securitypolicy(userid='pirate',
    #                                        permissive=False)
    #     request = testing.DummyRequest()
    #     request.context = testing.DummyResource()
    #     self.assertRaises(HTTPForbidden, viewtodo, request)


class FunctionalTests(unittest.TestCase):
    def setUp(self):
        # from todopiranhaform import main
        # app = main({}, **settings)
        from webtest import TestApp
        app = get_app('development.ini')
        self.testapp = TestApp(app)

    def test_root(self):
        resp = self.testapp.get('/login', status=200)
        # import ipdb; ipdb.set_trace()
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'Enter your username"', resp.body)
