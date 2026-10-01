from django import forms
from .models import Candidate


class CandidateForm(forms.ModelForm):

    class Meta:

        model = Candidate

        fields = [
            'enquiry_date',
            'candidate_name',
            'contact_no',
            'email',
            'gender',
            'dob',
            'qualification',
            'guardian_name',
            'guardian_contact_no',
            'address',
            'status',
            'remark',
        ]

        widgets = {

            'enquiry_date': forms.DateInput(
                attrs={'type': 'date'}
            ),

            'candidate_name': forms.TextInput(
                attrs={'placeholder': 'Enter candidate name'}
            ),

            'contact_no': forms.TextInput(
                attrs={'placeholder': 'Enter contact number'}
            ),

            'email': forms.EmailInput(
                attrs={'placeholder': 'Enter email address'}
            ),

            'dob': forms.DateInput(
                attrs={'type': 'date'}
            ),

            'qualification': forms.TextInput(
                attrs={'placeholder': 'Enter qualification'}
            ),

            'guardian_name': forms.TextInput(
                attrs={'placeholder': 'Enter father / guardian name'}
            ),

            'guardian_contact_no': forms.TextInput(
                attrs={'placeholder': 'Enter guardian contact number'}
            ),

            'address': forms.Textarea(
                attrs={
                    'rows': 3,
                    'placeholder': 'Enter complete address'
                }
            ),

            'remark': forms.Textarea(
                attrs={
                    'rows': 3,
                    'placeholder': 'Enter remarks'
                }
            ),
        }