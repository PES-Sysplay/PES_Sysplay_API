import django_tables2 as tables

from activity_action.models import ActivityJoined


class CheckinTable(tables.Table):

    class Meta:
        model = ActivityJoined
        attrs = {'class': 'table'}
        template = 'templates/checkin.html'
        fields = ['client__user__username', 'client__user__email', 'checked_in']
