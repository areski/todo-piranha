import unittest
import transaction
from pyramid.paster import get_app
from pyramid import testing
import os.path


here = os.path.dirname(__file__)


def _initTestingDB():
    from sqlalchemy import create_engine
    from .models import (
        DBSession,
        Base,
        Task,
        )
    engine = create_engine('sqlite://')
    Base.metadata.create_all(engine)
    DBSession.configure(bind=engine)
    with transaction.manager:
        model = Task(taskname='Learn 101 of telekinesis', status=False)
        DBSession.add(model)
        model = Task(taskname='Bend 20 forks', status=True)
        DBSession.add(model)
        model = Task(taskname='Become master in levitation', status=True)
        DBSession.add(model)
        model = Task(taskname='Go home flying', status=True)
        DBSession.add(model)
    return DBSession


# class DBSessionTests(unittest.TestCase):
#     @classmethod
#     def setUpClass(cls):
#         cls.session = _initTestingDB()
#         cls.config = testing.setUp()

#     @classmethod
#     def tearDownClass(cls):
#         cls.session.remove()
#         testing.tearDown()


class TodoViewTests(unittest.TestCase):
    def setUp(self):
        self.session = _initTestingDB()
        # self.config = testing.setUp()

    def tearDown(self):
        self.session.remove()
        # testing.tearDown()

    def test_passing_view(self):
        from .views import todo_json
        request = testing.DummyRequest()
        tasklist = todo_json(request)
        # import ipdb; ipdb.set_trace()
        # print(tasklist)
        self.assertEqual(tasklist[0].id, 1)
        self.assertEqual(tasklist[0].taskname, 'Learn 101 of telekinesis')

    def test_todofiltered_view(self):
        from .views import todofiltered
        request = testing.DummyRequest()
        # import ipdb; ipdb.set_trace()
        request.matchdict = {'viewtype': 'COMPLETED'}
        response = todofiltered(request)
        self.assertEqual(response['items_left'], 3)

    # def test_it_notsubmitted(self):
    #     # _registerRoutes(self.config)
    #     request = testing.DummyRequest()
    #     request.matchdict = {'pagename': 'AnotherPage'}
    #     info = self._callFUT(request)
    #     self.assertEqual(info['page'].data,'')
    #     self.assertEqual(info['save_url'],
    #                      'http://example.com/add_page/AnotherPage')


class TutorialViewTests(unittest.TestCase):
    def setUp(self):
        self.session = _initTestingDB()
        self.config = testing.setUp()

    def tearDown(self):
        self.session.remove()
        testing.tearDown()

    def test_todofiltered(self):
        from .views import todo_get

        request = testing.DummyRequest()
        request.matchdict = {'viewtype': 'COMPLETED'}
        response = todo_get(request)
        self.assertEqual(response['items_left'], 3)

    def test_todo_json(self):
        from .views import todo_json
        request = testing.DummyRequest()
        response = todo_json(request)
        self.assertEqual(len(response), 4)


# class TutorialAuthentication(unittest.TestCase):
#     def setUp(self):
#         self.config = testing.setUp()

#     def tearDown(self):
#         testing.tearDown()

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
        app = get_app(os.path.join(here, '../development.ini'))
        self.testapp = TestApp(app)

    def test_root(self):
        resp = self.testapp.get('/login', status=200)
        # import ipdb; ipdb.set_trace()
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'Enter your username"', resp.body)


class LoginFunctionalTests(unittest.TestCase):

    def setUp(self):
        self.session = _initTestingDB()
        self.config = testing.setUp()
        from pyramid.paster import get_app
        app = get_app(os.path.join(here, '../development.ini'))
        from webtest import TestApp
        self.testapp = TestApp(app)

    def tearDown(self):
        self.session.remove()
        testing.tearDown()
    def test_root(self):
        res = self.testapp.get('/', status=302)
        self.assertEqual(res.location, 'http://localhost/todo')

    # need to add login
    # def test_todo_page(self):
    #     res = self.testapp.get('/todo', status=200)
    #     self.assertTrue(b'Todo' in res.body)

    def test_unexisting_page(self):
        self.testapp.get('/SomePage', status=404)

    def test_successful_log_in(self):
        # import ipdb; ipdb.set_trace()
        res = self.testapp.get('/login')
        post_data = {
            'csrf_token': res.form['csrf_token'].value,
            'login': 'demo',
            'password': 'demo',
        }
        res = self.testapp.post('/login',
                            post_data,
                            xhr=True,
                            expect_errors=True)
        self.testapp.get('/todo', status=200)

    def test_wrong_log_in(self):
        res = self.testapp.get('/login')
        post_data = {
            'csrf_token': res.form['csrf_token'].value,
            'login': 'fakeuser',
            'password': 'nopassword',
        }
        res = self.testapp.post('/login',
                            post_data,
                            xhr=True,
                            expect_errors=True)
        self.testapp.get('/todo', status=403)
