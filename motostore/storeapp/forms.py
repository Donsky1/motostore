from django import forms
from .models import Motorcycle, Motorcycle_images


class MotorcycleForm(forms.ModelForm):
    class Meta:
        model = Motorcycle
        fields = '__all__'


MotorcycleImagesInlineFormSet = forms.inlineformset_factory(Motorcycle, Motorcycle_images, fields='__all__')
MotorcycleImagesInlineFormCreateSet = forms.inlineformset_factory(Motorcycle,
                                                                  Motorcycle_images,
                                                                  fields='__all__',
                                                                  extra=10)