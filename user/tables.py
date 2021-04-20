import django_tables2 as tables

from user.models import Organizer


class OrganizerTable(tables.Table):
    action = tables.TemplateColumn(template_name='include/delete_user_button.html')

    class Meta:
        model = Organizer
        attrs = {'class': 'table'}
        template = 'templates/organizer_list.html'
        fields = ['user__username', 'user__email', 'admin', 'action']
