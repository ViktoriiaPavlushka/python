from django.db.models import Avg, Min, Max, ExpressionWrapper, Count
from django.forms import IntegerField
from django.http import JsonResponse
from numpy.ma.extras import median

from cinema.models import Ticket, User, Film, Session, Hall, Price, Director, Genre
import pandas as pd
from datetime import date

current_year = date.today().year
today = date.today()

def userStatistic(request):
    stats = User.objects.annotate(
        age=ExpressionWrapper(
            (today.year - User('yearOfBirth__year')) -
            ((today.month, today.day) < (User('yearOfBirth__month'), User('yearOfBirth__day'))),
            output_field=IntegerField()
        )
    ).aggregate(
        count_users=Count('userID'),
        avg_age=Avg('age'),
        min_age=Min('age'),
        max_age=Max('age'),
        median_age = pd.Series(User.objects.values_list('age', flat=True)).median(),
    )
    return JsonResponse(stats)

def filmStatistic():
    stats = Film.objects.annotate(
        count_films = Count('filmID'),
        avg_minAge = Avg('minAge'),
        min_minAge = Min('minAge'),
        max_minAge = Max('minAge'),
        median_minAge = pd.Series(Film.objects.values_list('minAge', flat=True)).median(),
    )
    return JsonResponse(stats)

def PriceStatistic():
    stats = Price.objects.annotate(
        count_prices = Count('priceID'),
        avg_basePrice = Avg('basePrice'),
        avg_VIPPrice=Avg('VIPPrice'),
        min_basePrice = Min('basePrice'),
        min_VIPPrice=Min('VIPPrice'),
        max_basePrice = Max('basePrice'),
        max_VIPPrice=Max('ViPPrice'),
        median_basePrice = pd.Series(Price.objects.values_list('basePrice', flat=True)).median(),
        median_VIPPrice=pd.Series(Price.objects.values_list('VIPPrice', flat=True)).median(),
    )
    return JsonResponse(stats)

def HallStatistic():
    stats = Hall.objects.annotate(
        count_halls = Count('hallID'),
        avg_capacity = Avg('numberOfSeats'),
        min_capacity = Min('numberOfSeats'),
        max_capacity = Max('numberOfSeats'),
        median_capacity = pd.Series(Hall.objects.values_list('numberOfSeats', flat=True)).median(),
    )
    return JsonResponse(stats)