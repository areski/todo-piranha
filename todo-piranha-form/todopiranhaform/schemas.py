import colander


class TaskSchema(colander.MappingSchema):
    taskname = colander.SchemaNode(colander.String())
    status = colander.SchemaNode(colander.Boolean())

task_schema = TaskSchema()
