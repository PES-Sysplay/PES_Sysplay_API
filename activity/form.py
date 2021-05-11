from django import forms

from activity.models import Activity
from workout.mixins import BootstrapFormMixin
from workout.utils import get_fields

bootstrap_field_info = {'': {'fields': [{'name': 'name', 'space': 6},
                                        {'name': 'activity_type', 'space': 3},
                                        {'name': 'photo', 'space': 3},
                                        {'name': 'description', 'space': 12},
                                        {'name': 'start_date', 'space': 12},
                                        {'name': 'start_time', 'space': 6},
                                        {'name': 'duration', 'space': 6},
                                        {'name': 'location', 'space': 6},
                                        {'name': 'number_participants', 'space': 6},
                                        {'name': 'normal_price', 'space': 6},
                                        {'name': 'member_price', 'space': 6},
                                        {'name': 'only_member', 'space': 12},

                                        ], 'description': ''}, }


class ActivityForm(BootstrapFormMixin, forms.ModelForm):
    bootstrap_field_info = bootstrap_field_info
    photo = forms.FileField(required=False, label='Imagen')

    def clean_photo(self):
        photo = self.cleaned_data.get('photo', '')
        if not photo:
            self.add_error('photo', 'Imagen requerida')
        return photo

    class Meta:
        model = Activity
        fields = get_fields(bootstrap_field_info)
        labels = {
            'name': 'Nombre de la actividad',
            'activity_type': 'Tipo de actividad',
            'description': 'Descripción',
            'start_date': 'Fecha de inicio',
            'start_time': 'Hora de inicio',
            'duration': 'Duración de la actividad',
            'normal_price': 'Precio para no-socios',
            'member_price': 'Precio para socios',
            'number_participants': 'Número de participantes',
            'location': 'Lugar de la actividad',
            'only_member': 'Solo para socios'

        }
        help_texts = {
            'duration': 'En minutos',
            'location': 'En coordinadas. Ejemplo: 41.326371, 2.249145'
        }
        widgets = {
            'duration': forms.NumberInput(attrs={'id': 'form_homework', 'step': "0.01"}),
            'normal_price': forms.NumberInput(attrs={'id': 'form_homework', 'step': "0.01"}),
            'member_price': forms.NumberInput(attrs={'id': 'form_homework', 'step': "0.01"}),
            'start_date': forms.SelectDateWidget(),
            'start_time': forms.TimeInput(format="%H:%M"),
            'description': forms.Textarea(attrs={'row': 7}),
        }
