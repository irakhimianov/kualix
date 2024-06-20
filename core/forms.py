from django import forms


class Index(forms.Form):
    method = forms.CharField(label='Метод')
    params = forms.CharField(empty_value=None, required=False, label='Параметры метода')
