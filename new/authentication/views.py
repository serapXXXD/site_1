from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.core.paginator import Paginator
from django.views import View
from django.contrib.auth.decorators import login_required
from django.db.utils import IntegrityError
from .forms import RegisterUserForm, ProfileUserForm
from .models import Subscription
from blog.models import Post
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

User = get_user_model()


class LoginUserView(LoginView):
    form_class = AuthenticationForm
    template_name = 'login.html'


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'registration.html'
    success_url = reverse_lazy('authentication:login')


class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'profile.html'
    success_url = reverse_lazy('authentication:profile')
    form_class = ProfileUserForm

    def get_object(self, **kwargs):
        return self.request.user

    def form_valid(self, form):
        user = form.save()
        password = form.cleaned_data.get('password1')
        print(form.cleaned_data)
        if password != "" and password:
            user.set_password(password)
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subscribers'] = self.request.user.subscribers.all()
        context['subscriptions'] = self.request.user.subscriptions.all()
        return context


class SubscribeView(LoginRequiredMixin, View):
    def get(self, request, author_id):
        author = get_object_or_404(User, pk=author_id)

        if request.user != author:
            try:
                subscription = Subscription.objects.create(
                    subscriber=request.user, author=author)
            except IntegrityError:
                return render(request, 'sub_error.html', {'error': 'уже подписан'})
        else:
            return render(request, 'sub_error.html', {'error': 'на себя нельзя подписаться'})

        next = request.GET.get('next', 'blog:index')
        return redirect(next)


def unsubscribe_view(request, author_id):
    unsubscribe = Subscription.objects.filter(author_id=author_id, subscriber = request.user)

    if unsubscribe.exists():
        unsubscribe.delete()
    else:
        return render(request, 'sub_error.html', {'error': 'подписка не найдена!'})

    return redirect('blog:index')

@login_required
def subscribe_post_view(request):
    sub = Subscription.objects.filter(subscriber=request.user)
    if not sub.exists():
        return render(request, 'sub_error.html', {'error': 'Подписок ещё нет'})

    authors = [s.author for s in sub]
    object_list = Post.objects.filter(author__in=authors)
    paginator = Paginator(object_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'subscribe_list.html', {'page_obj': page_obj})
