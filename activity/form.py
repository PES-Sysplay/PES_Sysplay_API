from django import forms

from activity.models import Activity
from workout.mixins import BootstrapFormMixin


class ActivityForm(BootstrapFormMixin, forms.ModelForm):
    bootstrap_field_info = {'TITLE': {'fields': [{'name': 'name', 'space': 12}, ], 'description': 'DESCRIPTION'}, }

    class Meta:
        model = Activity
        fields = ('name', )
        labels = {
            'name': 'Full name'
        }
