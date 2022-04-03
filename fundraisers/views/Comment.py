from django.shortcuts import redirect, get_object_or_404
from django.views import View

from fundraisers.forms import CommentAddForm
from fundraisers.models import Fundraiser


class Add(View):
    def post(self, request, fundraiser_id):
        fundraiser = get_object_or_404(Fundraiser, pk=fundraiser_id)
        form = CommentAddForm(request.POST, fundraiser=fundraiser)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.fundraiser = fundraiser
            comment.user = None if request.user.is_anonymous else request.user
            comment.save()
        return redirect('fundraiser_detail', pk=fundraiser_id)
