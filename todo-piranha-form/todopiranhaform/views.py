from pyramid.response import Response
from pyramid.view import view_config
from .forms import myform

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    MyModel,
    )

conn_err_msg = "Pyramid is having a problem using your SQL database."


@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    try:
        one = DBSession.query(MyModel).filter(MyModel.name == 'one').first()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {'one': one, 'project': 'todo-piranha-form'}


@view_config(route_name='testjson', renderer='json')
def testjson(request):
    return {'val': 1}


@view_config(route_name='viewform', renderer='templates/viewform.jinja2')
def viewform(request):
    form = myform.render()
    return {
        'val': 1,
        'form': form
        }
