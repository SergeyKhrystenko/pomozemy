from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.urls import reverse_lazy

from fundraisers.models import Fundraiser, Comment, Transaction


class BaseModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))


class FundraiserForm(BaseModelForm):
    class Meta:
        model = Fundraiser
        fields = ['name', 'category', 'active', 'purpose', 'start_date', 'end_date', 'description']
        widgets = {
            'start_date': forms.DateTimeInput(format='%Y-%m-%dT%H:%M:%S', attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(format='%Y-%m-%dT%H:%M:%S', attrs={'type': 'datetime-local'}),
        }


class CommentAddForm(BaseModelForm):
    def __init__(self, *args, **kwargs):
        self.fundraiser = kwargs.pop('fundraiser')
        super().__init__(*args, **kwargs)
        self.helper.form_action = reverse_lazy('fundraiser_comment_add', kwargs={'fundraiser_id': self.fundraiser.pk})

    class Meta:
        model = Comment
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3, 'cols': 40}),
        }


class TransactionForm(BaseModelForm):
    def __init__(self, *args, **kwargs):
        self.fundraiser = kwargs.pop('fundraiser')
        super().__init__(*args, **kwargs)
        self.helper.form_action = reverse_lazy(
            'fundraiser_transaction_add',
            kwargs={'fundraiser_id': self.fundraiser.pk}
        )

    class Meta:
        model = Transaction
        fields = ['amount', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3, 'cols': 40}),
        }
