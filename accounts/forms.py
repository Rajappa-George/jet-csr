from django import forms
from django.contrib.auth.models import User


ROLE_CHOICES = [
    ('Admin', 'Admin'),
    ('Counsellor', 'Counsellor'),
    ('Trainer', 'Trainer'),
]


class UserCreateForm(forms.Form):

    full_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={'placeholder': 'Enter full name'}
        )
    )

    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={'placeholder': 'Enter username'}
        )
    )

    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(
            attrs={'placeholder': 'Enter email address'}
        )
    )

    contact_no = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': 'Enter contact number'}
        )
    )

    role = forms.ChoiceField(
        choices=ROLE_CHOICES
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Enter password'}
        )
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Confirm password'}
        )
    )

    def clean_username(self):

        username = self.cleaned_data['username']

        if User.objects.filter(
            username__iexact=username
        ).exists():
            raise forms.ValidationError(
                'This username already exists.'
            )

        return username

    def clean(self):

        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get(
            'confirm_password'
        )

        if (
            password and
            confirm_password and
            password != confirm_password
        ):
            self.add_error(
                'confirm_password',
                'Passwords do not match.'
            )

        return cleaned_data


class UserEditForm(forms.Form):

    full_name = forms.CharField(
        max_length=150
    )

    username = forms.CharField(
        max_length=150
    )

    email = forms.EmailField(
        required=False
    )

    contact_no = forms.CharField(
        max_length=15,
        required=False
    )

    role = forms.ChoiceField(
        choices=ROLE_CHOICES
    )

    def __init__(
        self,
        *args,
        user_instance=None,
        **kwargs
    ):

        super().__init__(*args, **kwargs)

        self.user_instance = user_instance

    def clean_username(self):

        username = self.cleaned_data['username']

        users = User.objects.filter(
            username__iexact=username
        )

        if self.user_instance:
            users = users.exclude(
                pk=self.user_instance.pk
            )

        if users.exists():
            raise forms.ValidationError(
                'This username already exists.'
            )

        return username