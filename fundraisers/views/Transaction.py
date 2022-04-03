from django.shortcuts import redirect, get_object_or_404
from django.views import View

from fundraisers.forms import TransactionForm
from fundraisers.models import Fundraiser


class Add(View):
    def post(self, request, fundraiser_id):
        fundraiser = get_object_or_404(Fundraiser, pk=fundraiser_id)
        form = TransactionForm(request.POST, fundraiser=fundraiser)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.fundraiser = fundraiser
            transaction.user = None if request.user.is_anonymous else request.user
            transaction.save()
        return redirect('fundraiser_detail', pk=fundraiser_id)
