from pyramid.view import view_config
from pyramid.view import forbidden_view_config
from pyramid.session import check_csrf_token
from pyramid.security import remember
from pyramid.security import forget
from .forms import TaskForm, LoginForm

from pyramid.httpexceptions import HTTPFound
from pyramid.httpexceptions import HTTPForbidden
# import deform
# from deform import ValidationFailure
# import colander
# from pyramid.response import Response
import datetime

from .usersdb import USERS

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    Task,
    )

conn_err_msg = "Pyramid is having a problem using your SQL database."

_TASKS = {}
_TASKS['default'] = [
    {
        "taskid": "1",
        "status": "COMPLETED",
        "description": "Learn 101 of telekinesis",
        "created": datetime.datetime.now().isoformat()
    },
    {
        "taskid": "2",
        "status": "ACTIVE",
        "description": "Bend 20 forks",
        "created": datetime.datetime.now().isoformat()
    },
    {
        "taskid": "3",
        "status": "ACTIVE",
        "description": "Become master in levitation",
        "created": datetime.datetime.now().isoformat()
    },
    {
        "taskid": "4",
        "status": "ACTIVE",
        "description": "Go home flying",
        "created": datetime.datetime.now().isoformat()
    },
]


def get_complete_task():
    # filter list
    return [task for task in _TASKS['default'] if task['status'] == 'ACTIVE']


def complete_task(taskid):
    # complete task
    ntasklist = []
    for task in _TASKS['default']:
        if task['taskid'] == taskid:
            task['status'] = "COMPLETED"
        ntasklist.append(task)
    return ntasklist


def delete_task(taskid):
    # delete task with taskid
    _TASKS['default'] = [task for task in _TASKS['default'] if task['taskid'] != taskid]


def count_items_left():
    count = 0
    for task in _TASKS['default']:
        if task['status'] == 'ACTIVE':
            count = count + 1
    return count


@view_config(route_name='todo_json', renderer='json',
             permission='view')
def todo_json(request):
    return _TASKS['default']


@view_config(route_name='todofiltered', renderer='templates/todo.jinja2',
             permission='view')
def todofiltered(request):
    viewtype = "ALL"
    if request.matchdict['viewtype']:
        viewtype = request.matchdict['viewtype'].upper()
    return todo_get(request, viewtype)


def filter_tasks(viewtype):
    if viewtype == 'ACTIVE' or viewtype == 'COMPLETED':
        return [task for task in _TASKS['default'] if task['status'] == viewtype]
    else:
        # Return all tasks
        return _TASKS['default']


@view_config(route_name='viewtodo', request_method="GET",
             renderer='templates/todo.jinja2', permission='view')
def todo_get(request, viewtype='ALL'):
    task = Task()
    form = TaskForm(obj=request.POST)
    if request.method == 'POST' and form.validate():
        form.populate_obj(task)
        DBSession.add(task)
        request.session.flash('Task added successfully', 'success')
        _TASKS['default'].append({
            "taskid": len(_TASKS['default']),
            "status": "ACTIVE",
            "description": form.taskname.data,
            "created": datetime.datetime.now().isoformat()
        })
    tasks = filter_tasks(viewtype)
    items_left = count_items_left()
    return dict(
        form=form,
        tasks=tasks,
        viewtype=viewtype,
        items_left=items_left,
        )


@view_config(route_name='viewtodo', request_method="POST",
             renderer='templates/todo.jinja2', permission='view')
def todo_post(request):
    form = TaskForm(request.POST)
    if request.method == 'POST' and form.validate():
        task = Task()
        form.populate_obj(task)
        DBSession.add(task)
        request.session.flash('Task added successfully', 'success')
        _TASKS['default'].append({
            "taskid": len(_TASKS['default']),
            "status": "ACTIVE",
            "description": form.taskname.data,
            "created": datetime.datetime.now().isoformat()
        })
    url = request.route_url('viewtodo')
    return HTTPFound(location=url)


@view_config(route_name='clear_completed')
def clear_completed(request):
    _TASKS['default'] = get_complete_task()
    url = request.route_url('viewtodo')
    return HTTPFound(location=url)


@view_config(route_name='task_delete')
def task_delete(request):
    if request.matchdict['taskid']:
        taskid = request.matchdict['taskid']
        delete_task(taskid)
        request.session.flash("Task deleted!", 'error')
    url = request.route_url('viewtodo')
    return HTTPFound(location=url)


@view_config(route_name='task_complete')
def task_complete(request):
    if request.matchdict['taskid']:
        taskid = request.matchdict['taskid']
        complete_task(taskid)
        request.session.flash("Task completed!", 'success')
    url = request.route_url('viewtodo')
    return HTTPFound(location=url)


@view_config(route_name='login', renderer='templates/login.jinja2')
def login(request):
    login_url = request.route_url('login')
    referrer = request.url
    if referrer == login_url:
        # never use the login form itself as came_from
        referrer = '/todo'
    came_from = request.params.get('came_from', referrer)
    message = ''
    login = ''
    password = ''
    # import ipdb; ipdb.set_trace()

    form = LoginForm(request.POST)
    if request.method == 'POST' and form.validate():
        # Require CSRF Token
        check_csrf_token(request)
        login = form.login.data
        password = form.password.data
        if USERS.get(login) == password:
            headers = remember(request, login)
            request.session.flash('Logged in successfully', 'success')
            return HTTPFound(location=came_from,
                             headers=headers)
        request.session.flash('Failed login', 'error')

    return dict(
        form=form,
        page_title="Login",
        message=message,
        url=request.application_url + '/login',
        came_from=came_from,
        login=login,
        password=password,
        )


@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    url = request.route_url('login')
    # url = request.resource_url(request.context)
    return HTTPFound(location=url,
                     headers=headers)


@view_config(route_name='home')
def homeview(request):
    url = request.route_url('viewtodo')
    return HTTPFound(location=url)


# @view_config(route_name='home', renderer='templates/mytemplate.pt')
# def my_view(request):
#     try:
#         one = DBSession.query(Task).filter(Task.taskname == 'one').first()
#     except DBAPIError:
#         return Response(conn_err_msg, content_type='text/plain', status_int=500)
#     return {'one': one, 'project': 'todo-piranha-form'}


# @forbidden_view_config(renderer='templates/login.jinja2')
# def forbidden(self):
#     """This special view renders a login page when a user requests
#     a page that they don't have permission to see. In the same way
#     that the notfound view is set up, this will fit nicely into our
#     global layout.
#     """
#     return {'section': 'login'}
