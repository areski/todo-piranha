from deform import Form
from .schemas import myform_schema


myform = Form(myform_schema, buttons=('submit',))
