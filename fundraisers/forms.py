from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from fundraisers.models import Fundraiser, Comment


class FundraiserForm(forms.ModelForm):
    class Meta:
        model = Fundraiser
        fields = ['name', 'description', 'purpose', 'active', 'start_date', 'end_date', 'category']
        widgets = {
            'start_date': forms.DateTimeInput(format='%Y-%m-%dT%H:%M:%S', attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(format='%Y-%m-%dT%H:%M:%S', attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))


class CommentAddForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['message']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))
