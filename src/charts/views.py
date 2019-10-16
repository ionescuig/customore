from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, TemplateView, View

from rest_framework.views import APIView
from rest_framework.response import Response

from .scraper_lazada import lazada
from .scraper_shopee import get_brands as shopee

from .forms import QuoteForm
from .models import Quote


def get_data(quote, results):
    for num_l, item in enumerate(lazada(quote, results), start=1):
        yield item, 'lazada', num_l
    for num_s, item in enumerate(shopee(quote, results), start=1):
        yield item, 'shopee', num_s


class HomeView(CreateView):
    template_name = 'home.html'
    form_class = QuoteForm

    def get_queryset(self):
        return Quote.objects.all()


class QuoteView(DetailView):
    model = Quote
    template_name = 'charts/charts.html'

    def get_queryset(self):
        return Quote.objects.all()

    def get_context_data(self, **kwargs):
        context = super(QuoteView, self).get_context_data(**kwargs)
        quote = Quote.objects.get(pk=1)
        context['quote'] = quote.quote
        context['results'] = quote.results
        return context


class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        brands = {}
        for item in get_data('son lì', 100):
            brand = item[0]
            if brand in brands:
                brands[brand] = {'shopee': brands[brand]['shopee'] + 1, 'lazada': brands[brand]['lazada'] + 1}
            else:
                if item[1] == 'shopee':
                    brands[brand] = {'shopee': 1, 'lazada': 0}
                elif item[1] == 'lazada':
                    brands[brand] = {'shopee': 0, 'lazada': 1}
        max_length = 0
        for brand in brands:
            if brands[brand]['shopee'] > max_length:
                max_length = brands[brand]['shopee']
            if brands[brand]['lazada'] > max_length:
                max_length = brands[brand]['lazada']
        if max_length // 5 > 0:
            max_length = max_length - max_length % 5 + 5

        data = {
            'labels': [brand for brand in brands],
            'shopee': [brands[brand]['shopee'] for brand in brands],
            'lazada': [brands[brand]['lazada'] for brand in brands],
            'max_brands': max_length,
        }
        return Response(data)
