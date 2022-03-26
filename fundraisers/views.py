from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.timezone import make_aware
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from datetime import datetime
from django.views import View

from fundraisers.models import Fundraiser, Category
from fundraisers.forms import FundraiserForm


class BaseFundraiserListView(ListView):
    model = Fundraiser
    template_name = 'fundraiser/fundraiser_list.html'
    ordering = ['-pk']


class FundraiserListView(BaseFundraiserListView):
    def get_queryset(self):
        return Fundraiser.objects.filter(
            active=True,
            start_date__lte=make_aware(datetime.now()),
            end_date__gte=make_aware(datetime.now()),
        )


class FundraiserMyListView(LoginRequiredMixin, BaseFundraiserListView):
    def get_queryset(self):
        return Fundraiser.objects.filter(
            owner=self.request.user,
        )


class FundraiserCategoryListView(BaseFundraiserListView):
    def get_queryset(self):
        return Fundraiser.objects.filter(
            category=get_object_or_404(Category, slug=self.kwargs['slug']),
            active=True,
            start_date__lte=make_aware(datetime.now()),
            end_date__gte=make_aware(datetime.now()),
        )


class FundraiserDetailView(DetailView):
    model = Fundraiser
    template_name = 'fundraiser/fundraiser_detail.html'


class FundraiserCreateView(LoginRequiredMixin, CreateView):
    model = Fundraiser
    form_class = FundraiserForm
    template_name = 'form.html'
    success_url = reverse_lazy('fundraiser_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class FundraiserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Fundraiser
    form_class = FundraiserForm
    template_name = 'form.html'

    def test_func(self):
        return self.request.user.pk == self.get_object().owner.pk

    def get_success_url(self):
        return reverse_lazy('fundraiser_update', args=[self.object.pk])


class CommentAddView(View):
    def post(self, request, fundraiser_id):

        fundraiser = Fundraiser.objects.get(pk=fundraiser_id)
        fundraiser.comment_set.create(
            user=None if request.user.is_anonymous else request.user,
            message=request.POST['comment']
        )
        return redirect('fundraiser_detail', pk=fundraiser_id)


class FundraiserVoteView(View):
    def post(self, request, fundraiser_id):
        fundraiser = Fundraiser.objects.get(pk=fundraiser_id)
        if request.POST['vote'] == 'up':
            fundraiser.upvote()
        elif request.POST['vote'] == 'down':
            fundraiser.downvote()
        return redirect('fundraiser_detail', pk=fundraiser_id)
