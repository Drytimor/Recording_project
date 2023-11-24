from django.contrib.auth.forms import BaseUserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field, Button, Div, MultiField
from crispy_forms.bootstrap import Modal
from django.urls import reverse_lazy
from .models import User


class CreateUserForm(BaseUserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
        )
        self.helper.form_id = 'create-user-form'
        self.helper.attrs = {
            'hx-post': reverse_lazy('create_user'),
            'hx-target': '#create-user-form',
            'hx-swap': 'outerHTML',
        }
        self.helper.add_input(Submit('submit', 'Зарегистрироваться'))

    class Meta(BaseUserCreationForm.Meta):

        model = User
        fields = ("username", "email")


