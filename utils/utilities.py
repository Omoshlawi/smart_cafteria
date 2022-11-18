def get_sql_fields(model):
    sql_fields = []
    for field in model.get_filed_name():
        f = getattr(model, field)
        sql_fields.append(f"{field} {f.getSqlType()}")
    return ", ".join(sql_fields)
