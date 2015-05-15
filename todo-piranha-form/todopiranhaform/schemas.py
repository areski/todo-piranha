import colander


class Myform(colander.MappingSchema):
    name = colander.SchemaNode(colander.String())
    age = colander.SchemaNode(colander.Integer(),
                              validator=colander.Range(0, 200))

myform_schema = Myform()