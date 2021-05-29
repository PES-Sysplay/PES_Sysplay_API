import django_tables2 as tables

from activity_action.models import ActivityJoined, ActivityReview


class CheckinTable(tables.Table):
    block = tables.TemplateColumn(template_name='include/actions.html', verbose_name='Sistema de bloqueo')

    class Meta:
        model = ActivityJoined
        attrs = {'class': 'table'}
        template = 'templates/checkin.html'
        fields = ['client__user__username', 'client__user__email', 'checked_in']


class ReviewTable(tables.Table):
    remove = tables.TemplateColumn(template_name='include/remove_review.html', verbose_name='Borrar comentario',
                                   orderable=False)

    class Meta:
        model = ActivityReview
        attrs = {'class': 'table'}
        template = 'templates/reviews.html'
        fields = ['joined__client__user__username', 'stars', 'comment', 'remove']
