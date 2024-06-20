from typing import Type

from django.forms import Form
from django.views.generic import FormView
from django.template.response import TemplateResponse

from core import datatools, forms


class Index(FormView):
    form_class = forms.Index
    template_name = 'index.html'
    success_url = '/'

    def form_valid(self, form: Type[Form]) -> TemplateResponse:
        data = form.cleaned_data
        client = datatools.Client()
        response = client.request(endpoint='api/v2/', **data)

        context = {'response': response}
        return self.render_to_response(context=context)
