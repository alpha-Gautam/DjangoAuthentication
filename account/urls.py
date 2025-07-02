from .models import User
from account.views import RegistrationView, ActivateView, TestAPI, LoginView, DeleteUserView, LogoutView, GetCSRFToken,UserDetailsView, UpdatePasswordView
from django.urls import path

urlpatterns = [
    path('account/test/', TestAPI.as_view(), name='test'),
    path('account/csrf/', GetCSRFToken.as_view(), name='get_csrf_token'),
    
    path('account/register/', RegistrationView.as_view(), name='register'),
    path('account/activate/<str:uid>/<str:token>/', ActivateView.as_view(), name='activate'),
    path('account/login/', LoginView.as_view(), name='login'),
    path('account/user/', UserDetailsView.as_view(), name='user_details'),
    path('account/update_password/', UpdatePasswordView.as_view(), name='update_password'),
    path('account/delete/', DeleteUserView.as_view(), name='delete_user'),
    # path('account/forgot_password/', ForgotPasswordView.as_view(), name='forgot_password'),
    # path('account/reset_password/<str:uid>/<str:token>/', ResetPasswordView.as_view(), name='reset_password'),
    path('account/logout/', LogoutView.as_view(), name='logout'),
]
