from deform import Form
from .schemas import task_schema


task_form = Form(task_schema, buttons=('submit',))
