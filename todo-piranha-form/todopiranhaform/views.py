from pyramid.response import Response
from pyramid.view import view_config
from .forms import task_form
from deform import ValidationFailure

import deform
import colander

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
        one = DBSession.query(TaskModel).filter(TaskModel.name == 'one').first()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {'one': one, 'project': 'todo-piranha-form'}


@view_config(route_name='testjson', renderer='json')
def testjson(request):
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


# @view_config(rroute_name='viewform2', renderer='templates/viewform.jinja2', name='sequence_of_mappings')
# def sequence_of_mappings(requesy):

#     class Person(colander.Schema):
#         name = colander.SchemaNode(colander.String())
#         age = colander.SchemaNode(colander.Integer(),
#                                   validator=colander.Range(0, 200))

#     class People(colander.SequenceSchema):
#         person = Person()

#     class Schema(colander.Schema):
#         people = People()

#     schema = Schema()
#     form = deform.Form(schema, buttons=('submit',))
