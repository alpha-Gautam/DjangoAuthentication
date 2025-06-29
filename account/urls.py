from .models import User
from account.views import RegistrationView, ActivateView
from django.urls import path

urlpatterns = [
    path('account/register/', RegistrationView.as_view(), name='register'),
    path('account/activate/<str:uid>/<str:token>/', ActivateView.as_view(), name='activate'),

]
