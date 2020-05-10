import random
import sys

from django.shortcuts import render
from django.views import View
from django.http import Http404
import plural_ru

import data


class MainView(View):
    def get(self, request):
    	random_tours = {x: data.tours[x] for x in random.sample(range(1, 17), 6)}
    	return render(request, 'index.html', {"tours": random_tours, 
    		"description": data.description, "subtitle": data.subtitle})


class DepartureView(View):
    def get(self, request, departure):
    	if departure not in data.departures:
    		raise Http404
    		
    	tours = {}
    	min_price = sys.maxsize
    	max_price = 0
    	min_nights = sys.maxsize
    	max_nights = 0

    	for tour in data.tours:
    		if departure == data.tours[tour]["departure"]:
    			tours[tour] = data.tours[tour]
    			min_price = min(min_price, tours[tour]["price"])
    			max_price = max(max_price, tours[tour]["price"])
    			min_nights = min(min_nights, tours[tour]["nights"])
    			max_nights = max(max_nights, tours[tour]["nights"])

    	num_turs = len(tours)
    	declension = plural_ru.ru(num_turs, ["тур", "тура", "туров"])
    	return render(request, 'departure.html', {"tours": tours, "departure": data.departures[departure],
    								"max_price": max_price, "min_price": min_price, "count": num_turs,
    								"max_nights": max_nights, "min_nights": min_nights, "declension": declension})


class TourView(View):
    def get(self, request, id):
    	if id not in data.tours:
    		raise Http404
    	departure = data.tours[id]["departure"]
    	return render(request, 'tour.html', {"tour": data.tours[id], "departure": data.departures[departure]})