from .views import *
from django.urls import path, include

urlpatterns = [

    path('', login_attempt, name="login"),
    path('register', register, name="register"),
    path('otp', otp, name="otp"),
    path('login-otp', login_otp, name="login_otp"),
    path('dashboard', dashboard, name="dashboard"),
    path('search-results/', search_results, name='search_results'),
    path('autocomplete/', autocomplete, name='autocomplete'),
    path('country-details/<str:code>/', country_details, name='country_details'),
    path('logout/', logout, name='logout'),

]