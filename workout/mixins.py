# Mixin for Django Forms that implements a way better look at forms
class BootstrapFormMixin:

    # example: {'TITLE': {'fields': [{'name': 'FIELD_NAME', 'space': 12},], 'description': 'DESCRIPTION'},}
    bootstrap_field_info = {}

    def set_read_only(self):
        for field in self.fields.values():
            field.disabled = True

    @property
    def is_read_only(self):
        for field in self.fields.values():
            if field.disabled:
                return True
        return False

    @property
    def get_fields(self):
        result = self.bootstrap_field_info
        for list_fields in result.values():
            sum = 0
            for field in list_fields.get('fields'):
                if sum + field.get('space') > 12:
                    sum = field.get('space')
                    field['new_row'] = True
                else:
                    sum += field.get('space')
                    field['new_row'] = False
                name = field.get('name')
                field.update({'field': self.fields.get(name).get_bound_field(self, name)})
        return result
