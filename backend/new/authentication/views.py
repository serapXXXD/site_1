from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import DetailView
from django.views import View
from django.contrib.auth.decorators import login_required
from django.db.utils import IntegrityError
from .forms import RegisterUserForm, ProfileUserForm, ProfileFromGoogleForm
from .models import Subscription, Like
from .mixins import ProfileMixin
from blog.models import Post
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

User = get_user_model()


class LoginUserView(LoginView):
    form_class = AuthenticationForm
    template_name = 'authentication/login.html'


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'authentication/registration.html'
    success_url = reverse_lazy('authentication:login')


class ProfileView(LoginRequiredMixin, ProfileMixin, DetailView):
    model = User
    template_name = 'authentication/profile.html'
    success_url = reverse_lazy('authentication:profile')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['likes_count'] = Like.objects.filter(liker=self.request.user).count()
        context['posts_count'] = Post.objects.filter(author=self.request.user).count()
        context['subscribers'] = self.request.user.subscribers.all().select_related('subscriber')
        context['subscriptions'] = self.request.user.subscriptions.all().select_related('author')
        return context


class ProfileEdit(LoginRequiredMixin, ProfileMixin, UpdateView):
    model = User
    template_name = 'authentication/profile_edit.html'
    success_url = reverse_lazy('authentication:profile')
    form_class = ProfileUserForm

    def form_valid(self, form):
        user = form.save()
        password = form.cleaned_data.get('password1')
        if password != "" and password:
            user.set_password(password)
        return super().form_valid(form)


class ProfileFromGoogleEdit(LoginRequiredMixin, ProfileMixin, UpdateView):
    model = User
    template_name = 'authentication/profile_from_google_edit.html'
    success_url = reverse_lazy('authentication:profile')
    form_class = ProfileFromGoogleForm


class SubscribeView(LoginRequiredMixin, View):
    def get(self, request, author_id):
        author = get_object_or_404(User, pk=author_id)

        if request.user != author:
            try:
                subscription = Subscription.objects.create(
                    subscriber=request.user, author=author)
            except IntegrityError:
                return render(request, 'authentication/sub_error.html', {'error': 'уже подписан'})
        else:
            return render(request, 'authentication/sub_error.html', {'error': 'на себя нельзя подписаться'})

        next = request.GET.get('next', 'blog:index')
        return redirect(next)


@login_required
def unsubscribe_view(request, author_id):
    unsubscribe = Subscription.objects.filter(author_id=author_id, subscriber=request.user)

    if unsubscribe.exists():
        unsubscribe.delete()
    else:
        return render(request, 'authentication/sub_error.html', {'error': 'подписка не найдена!'})

    return redirect('blog:index')
