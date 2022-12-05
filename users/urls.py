from django.urls import path

from users.views import registration, login, profile, logout

urlpatterns = [
    path('registration/', registration, name='registration'),

    path('login/', login, name='login'),
    path('profile/', profile, name='profile'),
    path('logout/', logout, name='logout'),
]
