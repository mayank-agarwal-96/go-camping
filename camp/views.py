# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import urllib

from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Avg
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .forms import SignUpForm, LoginForm
from .models import Camp, Rate
from watson import search as watson

# Create your views here.
def home(request):
    if(request.method == "POST"):
        data = [ x.strip(' ') for x in str(request.POST.get('search_term')).split(',')]
        search_text = " ".join(data)

        # data_params = {'city': None, 'state': None, 'country': None}
        # if len(data) == 3:
        #     data_params['city'] = data[0]
        #     data_params['state'] = data[1]
        #     data_params['country'] = data[2]

        # elif len(data) == 2:
        #     data_params['state'] = data[0]
        #     data_params['country'] = data[1]

        # elif len(data) == 1:
        #     data_params['country'] = data[0]

        data_params = {'query': search_text}
        return redirect("%s?%s" % (reverse('camp_list'), urllib.urlencode(data_params)))
        
    return render(request, "index.html")


def add_camp(request):
    if request.method == "POST":
        pass
    else:

        return render()


def camp_list(request):	

    data = request.GET
    # city = data.get('city')
    # state = data.get('state')
    # country = data.get('country')
    # qs = Camp.objects.all()
    # camps = qs
    # if state:
    #     camps = qs.filter(state__iexact=state)
    # if city:
    #     camps = qs.filter(city__iexact=city)

    search_text = data.get('query', "")
    camps = watson.filter(Camp, search_text)
    for camp in camps:
        ratings = Rate.objects.filter(camp=camp)
        average_rating = ratings.aggregate(Avg('rating'))['rating__avg']

        if average_rating:
            average_rating = round(average_rating, 1)
        camp.average_rating = average_rating
    
    return render(request, "camp_list.html", { 'camps': camps})


def camp_detail(request, slug=None):
    instance = get_object_or_404(Camp, slug=slug)
    ratings = Rate.objects.filter(camp=instance)
    average_rating = ratings.aggregate(Avg('rating'))['rating__avg']

    if average_rating:
        average_rating = round(average_rating, 1)    
    current_user_rating = None
    if request.user.is_authenticated():
        ratings = ratings.exclude(user=request.user)
        current_user_rating = Rate.objects.filter(user=request.user).filter(camp=instance).first()

        if current_user_rating:
            current_user_rating.stars = range(current_user_rating.rating)
            current_user_rating.posted_by = request.user.first_name + " " + request.user.last_name
        
    if len(ratings) > 5:
        ratings = ratings[:5]

    for rating in ratings:
        rating.stars = range(rating.rating)
        user = User.objects.get(username=rating.user)
        rating.posted_by = user.first_name + " " + user.last_name

    return render(request, "camp_detail.html", 
    	            {'camp': instance, 
    	            'ratings': ratings, 
    	            'current_user_rating': current_user_rating,
    	            'average_rating': average_rating})


@login_required(login_url='/camp/login/')
def post_review(request, slug=None):
    if request.method == "POST":
        camp = get_object_or_404(Camp, slug=slug)
        user = request.user

        rating = request.POST.get('user-rating')
        comment = request.POST.get('user-review')
        
        rate_obj = Rate(camp=camp, user=user, rating=rating, comment=comment)
        rate_obj.save()

        return redirect('camp_detail', slug=slug)

    else:
        return HttpResponse('NOT ALLOWED')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('camp_home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('camp_home')
        return redirect('login')

    else:
        return render(request, 'login.html', {'form': LoginForm()})


def landing(request):
    return render(request, 'landing.html')
