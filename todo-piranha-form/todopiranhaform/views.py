from pyramid.response import Response
from pyramid.view import view_config
from pyramid.view import forbidden_view_config
from pyramid.security import authenticated_userid
from pyramid.session import check_csrf_token
from pyramid.security import remember
from pyramid.security import forget
from .forms import task_form

from pyramid.httpexceptions import HTTPFound
from pyramid.httpexceptions import HTTPForbidden
from deform import ValidationFailure

import deform
import colander

from .usersdb import USERS

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    TaskModel,
    )

conn_err_msg = "Pyramid is having a problem using your SQL database."


def succeed():
    return Response('<div id="thanks">Thanks!</div>')


@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    try:
        one = DBSession.query(TaskModel).filter(TaskModel.taskname == 'one').first()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {'one': one, 'project': 'todo-piranha-form'}


@view_config(route_name='testjson', renderer='json')
def testjson(request):
    return {'val': 1}


@view_config(route_name='viewtodo', renderer='templates/todo.jinja2',
             permission='view')
def viewtodo(request):
    return {'val': 1}


@view_config(route_name='viewform', renderer='templates/viewform.jinja2')
def viewform(request):
    # import ipdb; ipdb.set_trace()
    appstruct = {}

    if 'submit' in request.POST:
        try:
            controls = request.POST.items()
            appstruct = task_form.validate(controls)
            html = task_form.render(appstruct)
        except deform.ValidationFailure as e:
            html = e.render()
    else:
        # the request requires a simple form rendering
        html = task_form.render()

    return {
        'form': html,
        'appstruct': appstruct,
        }


@view_config(renderer="templates/login.jinja2", context=HTTPForbidden)
@view_config(route_name='login', renderer='templates/login.jinja2')
def login(request):
    # login_url = request.resource_url(self.context, 'login')
    login_url = request.route_url('login')
    referrer = request.url
    if referrer == login_url:
        # never use the login form itself as came_from
        referrer = '/todo'
    came_from = request.params.get('came_from', referrer)
    message = ''
    login = ''
    password = ''
    if 'form.submitted' in request.params:
        # Require CSRF Token
        check_csrf_token(request)
        login = request.params['login']
        password = request.params['password']
        if USERS.get(login) == password:
            headers = remember(request, login)
            print("AUTHENTICATED!!!")
            request.session.flash('Logged in successfully', 'success')
            return HTTPFound(location=came_from,
                             headers=headers)
        message = 'Failed login'
    request.session.flash(message, 'error')

    return dict(
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


# @forbidden_view_config(renderer='templates/login.jinja2')
# def forbidden(self):
#     """This special view renders a login page when a user requests
#     a page that they don't have permission to see. In the same way
#     that the notfound view is set up, this will fit nicely into our
#     global layout.
#     """
#     return {'section': 'login'}
