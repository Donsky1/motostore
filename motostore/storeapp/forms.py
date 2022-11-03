from django import forms
from .models import Motorcycle, Motorcycle_images, Marks, \
    Moto_models, Moto_type, Displacement, City, Color, Transmission


class MotorcycleForm(forms.ModelForm):
    mark_info = forms.ModelChoiceField(queryset=Marks.objects.all(),
                                       label='Марка',
                                       widget=forms.Select(attrs={
                                           'class': 'form-control'
                                       }))
    model_info = forms.ModelChoiceField(queryset=Moto_models.objects.all(),
                                        label='Модель',
                                        widget=forms.Select(attrs={
                                            'class': 'form-control'
                                        }))
    moto_type = forms.ModelChoiceField(queryset=Moto_type.objects.all(),
                                       label='Тип мотоцикла',
                                       widget=forms.Select(attrs={
                                           'class': 'form-control'
                                       }))
    displacement = forms.ModelChoiceField(queryset=Displacement.objects.all(),
                                          label='Объем двигателя, см³',
                                          widget=forms.Select(attrs={
                                              'class': 'form-control'
                                          }))
    city = forms.ModelChoiceField(queryset=City.objects.all(),
                                  label='Город',
                                  widget=forms.Select(attrs={
                                      'class': 'form-control'
                                  }))
    color = forms.ModelChoiceField(queryset=Color.objects.all(),
                                   label='Цвет мотоцикла',
                                   widget=forms.Select(attrs={
                                       'class': 'form-control'
                                   }))
    mileage = forms.IntegerField(label='Пробег, км',
                                 widget=forms.NumberInput(attrs={
                                     'class': 'form-control',
                                     'min': 0
                                 }))
    horse_power = forms.IntegerField(label='Мощность, л.с',
                                     widget=forms.NumberInput(attrs={
                                         'class': 'form-control',
                                         'min': 0
                                     }))
    price = forms.IntegerField(label='Цена, руб',
                               widget=forms.NumberInput(attrs={
                                   'class': 'form-control',
                                   'min': 0
                               }))
    transmission = forms.ModelChoiceField(queryset=Transmission.objects.all(),
                                          label='Коробка передач',
                                          widget=forms.Select(attrs={
                                              'class': 'form-control'
                                          }))
    comment = forms.CharField(label='Комментарий',
                              widget=forms.Textarea(attrs={'class': 'form-control'}))

    field_order = ('mark_info', 'model_info', 'moto_type', 'displacement',
                   'horse_power', 'transmission', 'mileage', 'color', 'comment', 'city', 'price')

    class Meta:
        model = Motorcycle
        exclude = ('status', 'rate', 'user',)


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


MotorcycleImagesInlineFormSet = forms.inlineformset_factory(Motorcycle, Motorcycle_images, fields='__all__', extra=2)
MotorcycleImagesInlineFormCreateSet = forms.inlineformset_factory(Motorcycle,
                                                                  Motorcycle_images,
                                                                  fields='__all__',
                                                                  extra=10)
