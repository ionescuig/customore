import ast
from django.http import JsonResponse
from django.views.generic import CreateView, DetailView

from rest_framework.views import APIView
from rest_framework.response import Response

from .forms import QuoteForm
from .models import Quote

from .scraper_shopee import shopee_dict
from .scraper_lazada import lazada_dict


def collect_data(quote, results):
    brands_shopee, items_shopee = shopee_dict(quote, results)
    brands_lazada, items_lazada = lazada_dict(quote, results)
    brands = {}
    for brand in brands_shopee:
        brands[brand] = {'shopee': brands_shopee[brand], 'lazada': 0}
    for brand in brands_lazada:
        if brand in brands:
            brands[brand]['lazada'] = brands_lazada[brand]
        else:
            brands[brand] = {'shopee': 0, 'lazada': brands_lazada[brand]}
    return brands, items_shopee, items_lazada


class HomeView(CreateView):
    template_name = 'home.html'
    form_class = QuoteForm

    def get_queryset(self):
        return Quote.objects.all()

    def form_valid(self, form):
        quote = form.save(commit=False)
        search = quote.quote
        results = quote.results
        data, shopee, lazada = collect_data(search, results)
        quote.brands = data
        quote.items_shopee = shopee
        quote.items_lazada = lazada
        form.save()
        return super(HomeView, self).form_valid(form)


class QuoteView(DetailView):
    model = Quote
    template_name = 'charts/detail.html'

    def get_queryset(self):
        return Quote.objects.all()


class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        quote = Quote.objects.last()
        brands = ast.literal_eval(Quote.objects.last().brands)

        max_shopee = max([brands[brand]['shopee'] for brand in brands])
        max_lazada = max([brands[brand]['lazada'] for brand in brands])
        max_brands = max(max_shopee, max_lazada)

        data = {
            'quote': quote.quote,
            'results': quote.results,
            'labels': [brand for brand in brands],
            'shopee': [brands[brand]['shopee'] for brand in brands],
            'lazada': [brands[brand]['lazada'] for brand in brands],
            'items_shopee': quote.items_shopee,
            'items_lazada': quote.items_lazada,
            'max_brands': max_brands,
        }
        return Response(data)
