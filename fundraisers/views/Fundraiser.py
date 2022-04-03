from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.timezone import make_aware
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from fundraisers.forms import FundraiserForm, CommentAddForm, TransactionForm
from fundraisers.models import Fundraiser, Category


class BaseList(ListView):
    model = Fundraiser
    template_name = 'fundraiser/fundraiser_list.html'
    ordering = ['-pk']


class List(BaseList):
    def get_queryset(self):
        query_set = super().get_queryset()
        return query_set.filter(
            active=True,
            start_date__lte=make_aware(datetime.now()),
            end_date__gte=make_aware(datetime.now()),
        )


class MyList(LoginRequiredMixin, BaseList):
    def get_queryset(self):
        query_set = super().get_queryset()
        return query_set.filter(
            owner=self.request.user,
        )


class CategoryList(BaseList):
    def get_queryset(self):
        query_set = super().get_queryset()
        return query_set.filter(
            category=get_object_or_404(Category, slug=self.kwargs['slug']),
            active=True,
            start_date__lte=make_aware(datetime.now()),
            end_date__gte=make_aware(datetime.now()),
        )


class Detail(DetailView):
    model = Fundraiser
    template_name = 'fundraiser/fundraiser_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentAddForm(fundraiser=self.object)
        context['transaction_form'] = TransactionForm(fundraiser=self.object)
        return context


class Create(LoginRequiredMixin, CreateView):
    model = Fundraiser
    form_class = FundraiserForm
    template_name = 'form.html'
    success_url = reverse_lazy('fundraiser_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class Update(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Fundraiser
    form_class = FundraiserForm
    template_name = 'form.html'

    def test_func(self):
        return self.request.user.pk == self.get_object().owner.pk

    def get_success_url(self):
        return reverse_lazy('fundraiser_update', args=[self.object.pk])


class Vote(View):
    def post(self, request, fundraiser_id):
        fundraiser = get_object_or_404(Fundraiser, pk=fundraiser_id)
        if request.POST['vote'] == 'up':
            fundraiser.upvote()
        elif request.POST['vote'] == 'down':
            fundraiser.downvote()
        return redirect('fundraiser_detail', pk=fundraiser_id)
