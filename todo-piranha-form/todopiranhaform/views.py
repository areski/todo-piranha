from pyramid.view import view_config
from pyramid.view import forbidden_view_config
from pyramid.session import check_csrf_token
from pyramid.security import remember
from pyramid.security import forget
from .forms import TaskForm, LoginForm

from pyramid.httpexceptions import HTTPFound
from pyramid.httpexceptions import HTTPForbidden
import datetime

from .usersdb import USERS

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    Task,
    )

conn_err_msg = "Pyramid is having a problem using your SQL database."


def get_tasks(status):
    # filter list
    tasks = DBSession.query(Task).filter_by(status=status).all()
    return tasks


def get_all_tasks():
    # filter list
    tasks = DBSession.query(Task).all()
    return tasks


def complete_task(taskid):
    # complete task
    task = DBSession.query(Task).filter_by(id=taskid).one()
    task.status = False


def delete_task(taskid):
    # delete task with taskid
    task = DBSession.query(Task).filter_by(id=taskid).one()
    DBSession.delete(task)


def count_items_left():
    count = DBSession.query(Task).filter_by(status=True).count()
    return count


def filter_tasks(viewtype):
    if viewtype == 'ACTIVE':
        return get_tasks(True)
    elif viewtype == 'COMPLETED':
        return get_tasks(False)
    else:
        return get_all_tasks()


def get_login_came_from(request):
    login_url = request.route_url('login')
    referrer = request.url
    if referrer == login_url:
        # never use the login form itself as came_from
        referrer = '/todo'
    came_from = request.params.get('came_from', referrer)
    return came_from


@view_config(route_name='todo_json', renderer='json',
             permission='view')
def todo_json(request):
    return get_all_tasks()


@view_config(route_name='todofiltered', renderer='templates/todo.jinja2',
             permission='view')
def todofiltered(request):
    viewtype = "ALL"
    if request.matchdict['viewtype']:
        viewtype = request.matchdict['viewtype'].upper()
    return todo_get(request, viewtype)


@view_config(route_name='viewtodo', request_method="GET",
             renderer='templates/todo.jinja2', permission='view')
def todo_get(request, viewtype='ALL'):
    form = TaskForm()
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
        task = Task(taskname=form.taskname.data, status=True)
        form.populate_obj(task)
        DBSession.add(task)
        request.session.flash('Task added successfully', 'success')
    url = request.route_url('viewtodo')
    return HTTPFound(location=url)


@view_config(route_name='clear_completed')
def clear_completed(request):
    # ???
    # _TASKS['default'] = get_tasks(False)
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


@view_config(route_name='login', renderer='templates/login.jinja2',
             request_method="GET")
def login_get(request):
    came_from = get_login_came_from(request)
    form = LoginForm(request.POST)
    return dict(
        form=form,
        came_from=came_from,
        )


@view_config(route_name='login', renderer='templates/login.jinja2',
             request_method="POST")
def login_post(request):
    came_from = get_login_came_from(request)
    login = ''
    password = ''
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
        came_from=came_from,
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


# @forbidden_view_config(renderer='templates/login.jinja2')
# def forbidden(self):
#     """This special view renders a login page when a user requests
#     a page that they don't have permission to see. In the same way
#     that the notfound view is set up, this will fit nicely into our
#     global layout.
#     """
#     return {'section': 'login'}
