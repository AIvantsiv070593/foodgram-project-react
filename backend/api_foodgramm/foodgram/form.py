from django.forms import ModelForm
from django.forms.widgets import TextInput

from .models import Tags


class TagsForm(ModelForm):
    class Meta:
        model = Tags
        fields = '__all__'
        widgets = {
            'color': TextInput(attrs={'type': 'color'}),
        }
