def get_fields(form):
    fields = set()
    for fieldgroup in form.values():
        for field in fieldgroup['fields']:
            fields.add(field['name'])
    return fields
