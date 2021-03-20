from datetime import datetime

from django import forms

from activity.models import Activity
from workout.mixins import BootstrapFormMixin
from workout.utils import get_fields

bootstrap_field_info = {'TITLE': {'fields': [{'name': 'name', 'space': 12},
                                             {'name': 'description', 'space': 12},
                                             {'name': 'photo', 'space': 12},
                                             {'name': 'activity_type', 'space': 12},
                                             {'name': 'start_date', 'space': 12},
                                             {'name': 'start_time', 'space': 12},
                                             {'name': 'duration', 'space': 12},
                                             {'name': 'normal_price', 'space': 12},
                                             {'name': 'member_price', 'space': 12},
                                             {'name': 'number_participants', 'space': 12},
                                             {'name': 'status', 'space': 12},
                                             {'name': 'location', 'space': 12},
                                             {'name': 'only_member', 'space': 12}], 'description': 'DESCRIPTION'}, }


class ActivityForm(BootstrapFormMixin, forms.ModelForm):
    bootstrap_field_info = bootstrap_field_info
    start_date = forms.DateField(initial=datetime.now(), widget=forms.SelectDateWidget())
    start_time = forms.TimeField(initial=datetime.now())

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get("start_date")
        time = cleaned_data.get("start_time")
        date_time = datetime.combine(date, time)
        cleaned_data.update({"start_time": date_time})
        return cleaned_data

    class Meta:
        model = Activity
        fields = get_fields(bootstrap_field_info)
        labels = {
            'name': 'Nombre de la actividad',
            'description': 'Descripción',
            'photo': 'Adjuntar foto de actividad',
            'start_time': 'Fecha de inicio',
            'duration': 'Duración de la actividad',
            'normal_price': 'Precio para no-socios',
            'member_price': 'Precio para socios',
            'number_participants': 'Número de participantes',
            'status': 'status',
            'location': 'Lugar de la actividad',
            'only_member': 'Solo para socios'

        }

        widgets = {
            'duration': forms.NumberInput(attrs={'id': 'form_homework', 'step': "0.01"}),
            'normal_price': forms.NumberInput(attrs={'id': 'form_homework', 'step': "0.01"}),
            'member_price': forms.NumberInput(attrs={'id': 'form_homework', 'step': "0.01"})
        }
