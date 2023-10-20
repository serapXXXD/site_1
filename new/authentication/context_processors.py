from allauth.socialaccount.models import SocialAccount


def social_account(request):
    context = {'social_account': False}

    if request.user.is_authenticated:
        context['social_account'] = SocialAccount.objects.filter(user=request.user).exists()

    return context
