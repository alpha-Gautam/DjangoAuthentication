from .models import User
from account.views import RegistrationView, ActivateView, TestAPI, LoginView, LogoutView, GetCSRFToken
from django.urls import path

urlpatterns = [
    path('account/test/', TestAPI.as_view(), name='test'),
    path('account/csrf/', GetCSRFToken.as_view(), name='get_csrf_token'),
    
    path('account/register/', RegistrationView.as_view(), name='register'),
    path('account/activate/<str:uid>/<str:token>/', ActivateView.as_view(), name='activate'),
    path('account/login/', LoginView.as_view(), name='login'),
    path('account/logout/', LogoutView.as_view(), name='logout'),
]
