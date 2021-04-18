from django_tables2 import tables

from user.models import Organizer


class OrganizerTable(tables.Table):

    class Meta:
        model = Organizer
        attrs = {'class': 'table'}
        template = 'templates/organizer_list.html'
        fields = ['user__username', 'user__email', 'admin']
