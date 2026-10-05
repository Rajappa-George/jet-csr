from django import forms


class CallingTaskImportForm(forms.Form):

    excel_file = forms.FileField(
        label='Excel File',
        help_text=(
            'Upload .xlsx file with columns: '
            'S.No, Reg. No, Ref, Name, Mobile'
        )
    )

    def clean_excel_file(self):

        excel_file = self.cleaned_data[
            'excel_file'
        ]

        file_name = excel_file.name.lower()

        if not file_name.endswith('.xlsx'):

            raise forms.ValidationError(
                'Please upload an Excel .xlsx file.'
            )

        return excel_file