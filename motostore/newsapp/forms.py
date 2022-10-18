from django import forms
from .models import News


class CreateNewsForm(forms.ModelForm):
    class Meta:
        model = News
        exclude = ('author', )
        widgets = {
            'category': forms.CheckboxSelectMultiple
        }

