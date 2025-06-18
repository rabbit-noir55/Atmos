from django.urls import path
from .views import CustomGetApiView,Asus

urlpatterns = [
    path('hello/', CustomGetApiView.as_view()),
      path('ole/', Asus.as_view())
]