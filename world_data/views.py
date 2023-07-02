from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.models import User
from django.views.decorators.http import require_GET

from .models import *
import random
import requests
import http.client

from django.conf import settings
from django.contrib.auth import authenticate, login


# Create your views here.


def send_otp(mobile, otp):
    print("FUNCTION CALLED")
    authkey = settings.AUTH_KEY
    url = "https://control.msg91.com/api/v5/otp?mobile=" + mobile + "&template_id=your_template_id"

    payload = {
        "otp": f"{otp}",
        "message": f"Your otp is {otp}",
        "mobile": f"{mobile}"
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authkey": f"{authkey}"
    }

    response = requests.post(url, json=payload, headers=headers)

    print(response.text)

    return None


def login_attempt(request):
    if request.method == 'POST':
        mobile = request.POST.get('mobile')

        user = Profile.objects.filter(mobile=mobile).first()

        if user is None:
            context = {'message': 'User not found', 'class': 'danger'}
            return render(request, 'login.html', context)

        otp = str(random.randint(1000, 9999))
        user.otp = otp
        user.save()
        send_otp(mobile, otp)
        request.session['mobile'] = mobile
        return redirect('login_otp')
    return render(request, 'login.html')


def login_otp(request):
    mobile = request.session['mobile']
    context = {'mobile': mobile}
    if request.method == 'POST':
        otp = request.POST.get('otp')
        profile = Profile.objects.filter(mobile=mobile).first()

        if otp == profile.otp:
            user = User.objects.get(id=profile.user.id)
            login(request, user)
            return redirect('cart')
        else:
            context = {'message': 'Wrong OTP', 'class': 'danger', 'mobile': mobile}
            return render(request, 'login_otp.html', context)

    return render(request, 'login_otp.html', context)


def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')

        check_user = User.objects.filter(email=email).first()
        check_profile = Profile.objects.filter(mobile=mobile).first()

        if check_user or check_profile:
            context = {'message': 'User already exists', 'class': 'danger'}
            return render(request, 'register.html', context)

        user = User(email=email, first_name=name)
        user.save()
        otp = str(random.randint(1000, 9999))
        profile = Profile(user=user, mobile=mobile, otp=otp)
        profile.save()
        send_otp(mobile, otp)
        request.session['mobile'] = mobile
        return redirect('otp')
    return render(request, 'register.html')


def otp(request):
    mobile = request.session['mobile']
    context = {'mobile': mobile}
    if request.method == 'POST':
        otp = request.POST.get('otp')
        profile = Profile.objects.filter(mobile=mobile).first()

        if otp == profile.otp:
            return redirect('dashboard')
        else:
            print('Wrong')

            context = {'message': 'Wrong OTP', 'class': 'danger', 'mobile': mobile}
            return render(request, 'otp.html', context)

    return render(request, 'otp.html', context)


def dashboard(request):
    return render(request, 'dashboard.html')


@require_GET
def autocomplete(request):
    query = request.GET.get('term', '')
    suggestions = get_autocomplete_suggestions(query)
    return JsonResponse(suggestions, safe=False)


def search_results(request):
    query = request.GET.get('query', '')
    # Implement the logic to retrieve search results based on the query
    results = get_search_results(query)
    return render(request, 'search_results.html', {'results': results})


def country_details(request, code):
    country = get_object_or_404(Country, code=code)
    return render(request, 'country_details.html', {'country': country})


def logout(request):
    return redirect('login')


def get_autocomplete_suggestions(query):

    cities = City.objects.filter(name__icontains=query)
    countries = Country.objects.filter(name__icontains=query)
    languages = CountryLanguage.objects.filter(language__icontains=query)

    # Combine the results and format them as suggestions
    suggestions = []
    for city in cities:
        suggestions.append(city.name)
    for country in countries:
        suggestions.append(country.name)
    for language in languages:
        suggestions.append(language.language)

    return suggestions


def get_search_results(query):

    cities = City.objects.filter(name__icontains=query)
    countries = Country.objects.filter(name__icontains=query)
    languages = CountryLanguage.objects.filter(language__icontains=query)

    results = []

    # Collect the relevant information from the search results
    for city in cities:
        result = {
            'country': city.country,
            'city': city,
        }
        results.append(result)

    for country in countries:
        result = {
            'country': country,
            'city': None,
        }
        results.append(result)

    for language in languages:
        result = {
            'country': language.country,
            'city': None,
        }
        results.append(result)

    return results