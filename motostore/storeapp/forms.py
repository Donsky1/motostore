from django import forms
from .models import Motorcycle, Motorcycle_images


class MotorcycleForm(forms.ModelForm):
    class Meta:
        model = Motorcycle
        exclude = ('status', 'rate', 'user', )


class ContactForm(forms.Form):
    your_name = forms.CharField(max_length=20,
                                min_length=2,
                                required=True,
                                widget=forms.TextInput(attrs={
                                    'class': 'input',
                                    'id': 'name',
                                    'name': 'name'
                                }))
    email = forms.EmailField(required=True,
                             widget=forms.EmailInput(attrs={
                                 'name': 'email',
                                 'id': 'email',
                                 'class': 'input'
                             }))
    message = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'name': 'message',
        'id': 'message',
        'class': 'input'
    }))


MotorcycleImagesInlineFormSet = forms.inlineformset_factory(Motorcycle, Motorcycle_images, fields='__all__', extra=0)
MotorcycleImagesInlineFormCreateSet = forms.inlineformset_factory(Motorcycle,
                                                                  Motorcycle_images,
                                                                  fields='__all__',
                                                                  extra=10)
