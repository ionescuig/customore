from django.urls import path
from .views import ChartData

urlpatterns = [
    path('chart/data/', ChartData.as_view(), name='chart_data'),
]
