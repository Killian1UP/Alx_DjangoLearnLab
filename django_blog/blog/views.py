from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm, UserProfileForm
from .models import UserProfile
# Create your views here.
class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'blog/register.html'

    def form_valid(self, form):
        user = form.save()
        user_profile = UserProfile(user=user)
        user_profile.save()
        return super().form_valid(form)

@login_required
def profile_view(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile(user=request.user)
        user_profile.save()
    
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=request.user)
        user_profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)

        if profile_form.is_valid() and user_profile_form.is_valid():
            profile_form.save()
            user_profile_form.save()
            return redirect('profile')
    else:
        profile_form = ProfileForm(instance=request.user)
        user_profile_form = UserProfileForm(instance=user_profile)

    context = {
        'profile_form': profile_form,
        'user_profile_form': user_profile_form,
    }
    return render(request, 'blog/profile.html', context)

