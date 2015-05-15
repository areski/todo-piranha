import colander


class TaskSchema(colander.MappingSchema):
    taskname = colander.SchemaNode(colander.String(),
                                  validator=colander.OneOf(['task', 'work']))
    status = colander.SchemaNode(colander.Boolean())

task_schema = TaskSchema()
