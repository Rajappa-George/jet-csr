from django import forms
from django.contrib.auth.models import User

from .models import Candidate


class CandidateForm(forms.ModelForm):

    class Meta:

        model = Candidate

        fields = [
            'enquiry_date',
            'counsellor',
            'candidate_name',
            'contact_no',
            'gender',
            'qualification',
            'guardian_name',
            'location',
            'other_location',
            'address',
            'course_interested',
            'family_annual_income',
            'skill_preference',
            'status',
            'remark',
        ]

        widgets = {

            'enquiry_date': forms.DateInput(
                attrs={
                    'type': 'date'
                }
            ),

            'candidate_name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter candidate name'
                }
            ),

            'contact_no': forms.TextInput(
                attrs={
                    'placeholder': 'Enter 10 digit contact number',
                    'maxlength': '10',
                    'minlength': '10',
                    'pattern': '[0-9]{10}',
                    'inputmode': 'numeric',
                }
            ),

            'guardian_name': forms.TextInput(
                attrs={
                    'placeholder':
                        'Enter father / guardian name'
                }
            ),

            'other_location': forms.TextInput(
                attrs={
                    'placeholder':
                        'Enter other location'
                }
            ),

            'address': forms.Textarea(
                attrs={
                    'rows': 3,
                    'placeholder':
                        'Enter complete address'
                }
            ),

            'family_annual_income': forms.NumberInput(
                attrs={
                    'placeholder':
                        'Enter annual income',
                    'min': '0',
                    'step': '1',
                    'inputmode': 'numeric',
                }
            ),

            'remark': forms.Textarea(
                attrs={
                    'rows': 3,
                    'placeholder':
                        'Enter remarks'
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields['counsellor'].queryset = (
            User.objects.filter(
                profile__role='Counsellor',
                is_active=True
            ).order_by(
                'first_name',
                'username'
            )
        )

        self.fields['counsellor'].required = True

        self.fields['counsellor'].empty_label = (
            'Select Counsellor'
        )

        self.fields['gender'].empty_label = (
            'Select Gender'
        )

        self.fields['qualification'].empty_label = (
            'Select Qualification'
        )

        self.fields['location'].empty_label = (
            'Select Location'
        )

        self.fields['course_interested'].empty_label = (
            'Select Course'
        )

        self.fields['skill_preference'].empty_label = (
            'Select Skill Preference'
        )

        self.fields['status'].empty_label = (
            'Select Status'
        )

    def clean_contact_no(self):

        contact_no = (
            self.cleaned_data
            .get('contact_no', '')
            .strip()
        )

        if not contact_no.isdigit():

            raise forms.ValidationError(
                'Contact number must contain numbers only.'
            )

        if len(contact_no) != 10:

            raise forms.ValidationError(
                'Contact number must contain exactly 10 digits.'
            )

        return contact_no

    def clean(self):

        cleaned_data = super().clean()

        location = cleaned_data.get('location')

        other_location = (
            cleaned_data.get('other_location') or ''
        ).strip()

        if location == 'Others' and not other_location:

            self.add_error(
                'other_location',
                'Please enter the location.'
            )

        if location != 'Others':

            cleaned_data['other_location'] = ''

        return cleaned_data