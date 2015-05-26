import unittest
import transaction

from pyramid.paster import get_app

from pyramid import testing


def _initTestingDB():
    from sqlalchemy import create_engine
    from .models import (
        DBSession,
        Base,
        TaskModel,
        )
    engine = create_engine('sqlite://')
    Base.metadata.create_all(engine)
    DBSession.configure(bind=engine)
    with transaction.manager:
        model = TaskModel(taskname='mytask-test', status=True)
        DBSession.add(model)
    return DBSession


class TodoViewTests(unittest.TestCase):
    def setUp(self):
        self.session = _initTestingDB()
        self.config = testing.setUp()

    def tearDown(self):
        self.session.remove()
        testing.tearDown()

    def test_passing_view(self):
        from .views import todo_json
        request = testing.DummyRequest()
        tasklist = todo_json(request)
        self.assertEqual(tasklist[0]['taskid'], '1')
        self.assertEqual(tasklist[0]['description'], 'Learn 101 of telekinesis')

    def test_todofiltered_view(self):
        from .views import todofiltered
        request = testing.DummyRequest()
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


# --

class LoginFunctionalTests(unittest.TestCase):

    viewer_login = '/login?login=demo&password=demo' \
                   '&form.submitted=Login'
    viewer_wrong_login = '/login?login=demo&password=incorrect' \
                         '&form.submitted=Login'

    def setUp(self):
        from todopiranhaform import main
        settings = {'sqlalchemy.url': 'sqlite://'}
        app = main({}, **settings)
        from webtest import TestApp
        self.testapp = TestApp(app)
        # _initTestingDB()

    def tearDown(self):
        del self.testapp
        from .models import DBSession
        DBSession.remove()

    def test_root(self):
        res = self.testapp.get('/', status=302)
        self.assertEqual(res.location, 'http://localhost/todo')

    def test_todo_page(self):
        res = self.testapp.get('/todo', status=200)
        self.assertTrue(b'Todo' in res.body)

    def test_unexisting_page(self):
        self.testapp.get('/SomePage', status=404)

    def test_successful_log_in(self):
        res = self.testapp.get('/login')
        post_data = {
            'csrf_token': res.form['csrf_token'].value
        }
        res = self.testapp.post(self.viewer_login,
                            post_data,
                            xhr=True,
                            expect_errors=True)
        # import ipdb; ipdb.set_trace()
        self.testapp.get('/todo', status=200)
