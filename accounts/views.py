from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from accounts.forms import LoginForm, UserCreateForm


class LoginView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_anonymous

    def get(self, request):
        return render(request, 'form.html', {'form': LoginForm()})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                redirect_url = request.GET.get('next', 'index')
                return redirect(redirect_url)
            return render(request, 'form.html', {'form': form})


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('index')


class UserCreate(UserPassesTestMixin, CreateView):
    form_class = UserCreateForm
    template_name = 'form.html'
    success_url = reverse_lazy('index')

    def test_func(self):
        return self.request.user.is_anonymous

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        authenticated_user = authenticate(self.request, username=email, password=password)
        login(self.request, authenticated_user)
        return redirect(self.success_url)
