from django import forms
from .models import News, Category


class CreateNewsForm(forms.ModelForm):
    title = forms.CharField(label='Заголовок',
                            widget=forms.TextInput(attrs={
                                'class': 'form-control',
                            }))
    category = forms.ModelMultipleChoiceField(label='Категория новости',
                                              widget=forms.SelectMultiple(attrs={
                                                  'class': 'form-control'
                                              }),
                                              queryset=Category.objects.all())

    text = forms.CharField(label='Описание новости',
                           widget=forms.Textarea(attrs={
                               'class': 'form-control',
                           }))
    link = forms.CharField(label='Ссылка на видео',
                           widget=forms.TextInput(attrs={
                               'class': 'form-control'
                           }),
                           required=False)
    image = forms.ImageField(label='Изображение')

    class Meta:
        model = News
        exclude = ('author',)
        widgets = {
            'category': forms.CheckboxSelectMultiple,
        }
