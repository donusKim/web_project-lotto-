from django.urls import path
from catalog import views

urlpatterns = [
    path('', views.index, name='index'),
    path('rounds/', views.roundListView.as_view(), name='rounds'),
    path('round/<int:pk>', views.roundDetailView.as_view(), name='round-detail'),
]