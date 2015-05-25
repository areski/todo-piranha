import unittest
import transaction

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

    def test_todofiltered(self):
        from .views import viewtodo

        request = testing.DummyRequest()
        request.matchdict = {'viewtype': 'COMPLETED'}
        response = viewtodo(request)
        self.assertEqual(response.status_code, 200)
