import django_tables2 as tables

from user.models import Organizer, Organization


class OrganizerTable(tables.Table):
    action = tables.TemplateColumn(template_name='include/delete_user_button.html')

    class Meta:
        model = Organizer
        attrs = {'class': 'table'}
        template = 'templates/organizer_list.html'
        fields = ['user__username', 'user__email', 'admin', 'action']


class OrganizationTable(tables.Table):
    name = tables.Column(orderable=False, verbose_name='Organización')
    rank = tables.Column(orderable=False, verbose_name='Puntuación')
    superhost = tables.Column(orderable=False)

    class Meta:
        model = Organization
        attrs = {'class': 'table'}
        template = 'templates/ranking.html'
        fields = ['name', 'rank', 'superhost']
