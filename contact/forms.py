from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from . import models


class ContactForm(forms.ModelForm):
    # muda os widgets de 3 jeitos diferentes, sobrescreve os models
    # first_name = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={
    #             'class': 'class-a class-b',
    #             'placeholder': 'Write here',
    #         }
    #     ),
    #     label='first name',
    #     help_text='help text for the user',
    # )

    # cria um novo campo que nao esta no model
    # any = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={
    #             'class': 'class-a class-b',
    #             'placeholder': 'Write here',
    #         }
    #     ),
    #     label='any any',
    #     help_text='help text for the user',
    # )

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    # atualiza os widgets
    # self.fields['first_name'].widget.attrs.update(
    #     {
    #         'class': 'class-a class-b',
    #         'placeholder': 'Write here init',
    #     }
    # )

    picture = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                'accept': 'image/*',

            }
        ),
        required=False
    )

    class Meta:
        model = models.Contact
        fields = (
            'first_name', 'last_name', 'phone',
            'email', 'description', 'category',
            'picture',
        )

        # cria novos widgets
        # widgets = {
        #     'first_name': forms.TextInput(
        #         attrs={
        #             'class': 'class-a class-b',
        #             'placeholder': 'Write here',
        #         }
        #     )
        # }

    def clean(self):
        cleaned_data = self.cleaned_data
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')

        if first_name == last_name:
            msg = ValidationError(
                'Primeiro nome não pode ser igual ao segundo',
                code='invalid'
            )
            self.add_error('first_name', msg)
            self.add_error('last_name', msg)

        # self.add_error(
        #     # 'first_name',
        #     None,
        #     ValidationError(
        #         'Error msg',
        #         code='invalid'
        #     )
        # )

        # self.add_error(
        #     'first_name',
        #     ValidationError(
        #         'Error msg 2',
        #         code='invalid'
        #     )
        # )

        return super().clean()

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')

        # raise para o codigo e nao leo que esta abaixo, melhor usar add_error
        # if first_name == 'ABC':
        #     raise ValidationError(
        #         'No ABC here',
        #         code='invalid'
        #     )

        if first_name == 'ABC':
            self.add_error(
                'first_name',
                ValidationError(
                    'No ABC here',
                    code='invalid'
                )
            )

        return first_name


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        required=True,
        min_length=3,

    )

    last_name = forms.CharField(
        required=True,
        min_length=3,

    )

    email = forms.EmailField(

    )

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email',
            'username', 'password1', 'password2',
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            self.add_error(
                'email',
                ValidationError('this e-mail is being used', code='invalid')
            )
        return email


class RegisterUpdateForm(forms.ModelForm):
    first_name = forms.CharField(
        min_length=2,
        max_length=30,
        required=True,
        help_text='Required.',
        error_messages={
            'min_length': 'Please, add more than 2 letters.'
        }
    )
    last_name = forms.CharField(
        min_length=2,
        max_length=30,
        required=True,
        help_text='Required.'
    )

    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
        required=False,
    )

    password2 = forms.CharField(
        label="Password 2",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text='Use the same password as before.',
        required=False,
    )

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email',
            'username',
        )

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 or password2:
            if password1 != password2:
                self.add_error(
                    'password2',
                    ValidationError('the passwords are not the same')
                )

    def save(self, commit=True):
        cleaned_data = self.cleaned_data
        user = super().save(commit=False)
        password = cleaned_data.get('password1')

        if password:
            user.set_password(password)

        if commit:
            user.save()

        return user

    def clean_email(self):
        email = self.cleaned_data.get('email')
        current_email = self.instance.email

        if current_email != email:
            if User.objects.filter(email=email).exists():
                self.add_error(
                    'email',
                    ValidationError(
                        'this e-mail is being used', code='invalid')
                )

        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        if password1:
            try:
                password_validation.validate_password(password1)
            except ValidationError as errors:
                self.add_error(
                    'password1',
                    ValidationError(errors)
                )

        return password1
