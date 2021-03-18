from django import forms

from activity.models import Activity
from workout.mixins import BootstrapFormMixin


class ActivityForm(BootstrapFormMixin, forms.ModelForm):
    bootstrap_field_info = {'TITLE': {'fields': [{'name': 'name', 'space': 12},
                                                 {'name': 'description', 'space': 12},
                                                 {'name': 'photo', 'space': 12},
                                                 {'name': 'start_time', 'space': 12},
                                                 {'name': 'duration', 'space': 12},
                                                 {'name': 'normal_price', 'space': 12},
                                                 {'name': 'member_price', 'space': 12},
                                                 {'name': 'number_participants', 'space': 12},
                                                 {'name': 'status', 'space': 12},
                                                 {'name': 'location', 'space': 12},
                                                 {'name': 'only_member', 'space': 12}], 'description': 'DESCRIPTION'}, }

    class Meta:
        model = Activity
        fields = ('name', 'description', 'photo', 'start_time', 'duration', 'normal_price', 'member_price',
                  'number_participants', 'status', 'location', 'only_member')
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
            'start_time': forms.SelectDateWidget(),
            'duration': forms.NumberInput(attrs={'id': 'form_homework', 'step': "0.01"}),
            'normal_price': forms.NumberInput(attrs={'id': 'form_homework', 'step': "0.01"}),
            'member_price': forms.NumberInput(attrs={'id': 'form_homework', 'step': "0.01"})
        }
