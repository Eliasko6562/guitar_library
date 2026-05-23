from django.urls import path
from .views import GuitarListView, GuitarDetailView

urlpatterns = [
    path('', GuitarListView.as_view(), name='guitar-list'),
    path('guitar/<int:pk>/', GuitarDetailView.as_view(), name='guitar-detail'),
]
