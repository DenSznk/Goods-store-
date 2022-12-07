from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth, messages
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, TemplateView

from products.models import Basket
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from users.models import User, EmailVerification


def login(request):
    """Login after registration"""

    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
    else:
        form = UserLoginForm()
    context = {
        'form': form,
    }
    return render(request, 'users/login.html', context)


# class UserRegistrationView(CreateView):
#     model = User
#     form_class = UserRegistrationForm
#     template_name = 'users/registration.html'
#     success_url = reverse_lazy('user:login')
#
#     def get_context_data(self, **kwargs):
#         context = super(UserRegistrationView, self).get_context_data()
#         context['title'] = 'Store Registration'
#         return context
#
#
# class UserProfileView(LoginRequiredMixin, UpdateView):
#     model = User
#     form_class = UserProfileForm
#     template_name = 'users/profile.html'
#
#     def get_success_url(self):
#         return reverse_lazy('user:profile', args=(self.object.id,))
#
#     def get_context_data(self, **kwargs):
#         context = super(UserProfileView, self).get_context_data()
#         context['title'] = 'User Profile'
#         context['baskets'] = Basket.objects.filter(user=self.request.user)
#         return context


def registration(request):
    """Create USER """

    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You are welcome!')
            return HttpResponseRedirect(reverse('login'))
    else:
        form = UserRegistrationForm()
    context = {'form': form}
    return render(request, 'users/registration.html', context)


@login_required
def profile(request):
    """Personal account of a registered user"""

    if request.method == 'POST':
        form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('profile'))
    else:
        form = UserProfileForm(instance=request.user)
    context = {
        'title': 'Store - Profile',
        'form': form,
        'baskets': Basket.objects.filter(user=request.user)
    }
    return render(request, 'users/profile.html', context)


def logout(request):
    """Sign out of account"""

    auth.logout(request)
    return HttpResponseRedirect(reverse('login'))


class EmailVerificationView(TemplateView):
    title = 'store verification_email'
    template_name = 'users/email_verification.html'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_verifications = EmailVerification.objects.filter(user=user, code=code)
        if email_verifications.exist():
            user.is_verified_email = True
            user.save()
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('index'))
