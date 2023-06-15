from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, ModelFormMixin, DeleteView
from django.core.paginator import Paginator
from django.views import View
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


class ProfileView(LoginRequiredMixin, UpdateView, ModelFormMixin):
    model = User
    template_name = 'profile.html'
    success_url = reverse_lazy('authentication:profile')
    form_class = ProfileUserForm

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        user = form.save()
        password = form.cleaned_data.get('password1')
        print(form.cleaned_data)
        if password != "" and password:
            user.set_password(password)
        return super().form_valid(form)


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
    unsubscribe = get_object_or_404(Subscription, author_id=author_id)

    if request.user != unsubscribe:
        unsubscribe.delete()
    else:
        return render(request, 'sub_error.html', {'error': 'от себя не отпидсаться!'})

    return redirect('blog:index')


def subscribe_list_view(request):
    try:
        sub = Subscription.objects.get(subscriber=request.user.id)
    except:
        return render(request, 'sub_error.html', {'error': 'Подписок ещё нет'})

    object_list = Post.objects.filter(author=sub.author_id)
    paginator = Paginator(object_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'subscribe_list.html', {'page_obj': page_obj})
