from django.contrib.auth import login, authenticate, logout
from account.models import User
from account.serializers import UserSerializer
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.utils.decorators import method_decorator
from django.conf import settings
from account.utils import send_activation_email, send_reset_password_email


class TestAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        return Response({"message": "API is working!"}, status=status.HTTP_200_OK)
    
@method_decorator(ensure_csrf_cookie, name='dispatch')
class GetCSRFToken(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"csrfToken": request.META.get('CSRF_COOKIE', '')}, status=status.HTTP_200_OK)
    
class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.create(serializer.validated_data)
            # Send Account Activation Email
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            activation_link = reverse('activate', kwargs={'uid':uid, 'token':token})
            activation_url = f'{settings.SITE_DOMAIN}{activation_link}'
            print("activation linl--",activation_link)
            print("activation url--",activation_url)
            send_activation_email(user.email, activation_url)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
class ActivateView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, uid, token):
        try:
            uid = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and default_token_generator.check_token(user, token):
            if user.is_active:
                return Response({"message": "Account is already activated."}, status=status.HTTP_200_OK)
            user.is_active = True
            user.save()
            return Response({"message": "Account activated successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Activation link is invalid or has expired."}, status=status.HTTP_400_BAD_REQUEST)
        

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
       
        email = request.data.get('email')
        password = request.data.get('password')
        user = User.objects.filter(email=email).first()
        if user is not None and user.is_active == False:
            return Response({"error": "Account is not activated. Please check your email for the activation link."}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return Response({"message": "Login successful."}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST)   
    
class UserDetailsView(APIView):
    # permission_classes = [AllowAny]

    def get(self, request):
        user = request.user
        if user.is_authenticated:
            serializer = UserSerializer(user)
            data= serializer.data
            data["is_staff"] = user.is_staff
            return Response(data, status=status.HTTP_200_OK)
        return Response({"error": "User not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)   
    
    
    def patch(self, request):
        user = request.user
        if user.is_authenticated:
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "User not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)
    
    
class UpdatePasswordView(APIView):
    # permission_classes = [AllowAny]

    def post(self, request):
        user = request.user
        if user.is_authenticated:
            old_password = request.data.get('old_password')
            new_password = request.data.get('new_password')
            confirm_password = request.data.get('confirm_password')
            if not user.check_password(old_password):
                return Response({"error": "Old password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)
            if new_password != confirm_password:
                return Response({"error": "Passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(new_password)
            user.save()
            return Response({"message": "Password updated successfully."}, status=status.HTTP_200_OK)
        return Response({"error": "User not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)
    
class DeleteUserView(APIView):
    # permission_classes = [AllowAny]

    def delete(self, request):
        user = request.user
        if user.is_authenticated:
            user.delete()
            logout(request)
            return Response({"message": "User deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "User not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    # permission_classes = [AllowAny]

    def post(self, request):
        logout(request)
        return Response({"message": "Logout successful."}, status=status.HTTP_200_OK)
 
 
class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_link = reverse('reset_password', kwargs={'uid': uid, 'token': token})
            reset_url = f'{settings.SITE_DOMAIN}{reset_link}'
            send_reset_password_email(user.email, reset_url)  # Implement this function to send the email
            return Response({"message": "Password reset link sent to your email."}, status=status.HTTP_200_OK)
        return Response({"error": "Email not found."}, status=status.HTTP_404_NOT_FOUND)
    
class ResetPasswordPageView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uid, token):
        # Render the password reset page
        print("password reset page opened")
        return render(request, 'account/reset_password_page.html', {'uid': uid, 'token': token})

    def post(self, request, uid, token):
        try:
            uid = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and default_token_generator.check_token(user, token):
            new_password = request.data.get('new_password')
            confirm_password = request.data.get('confirm_password')
            if new_password != confirm_password:
                return Response({"error": "Passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(new_password)
            user.save()
            return Response({"message": "Password reset successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Reset link is invalid or has expired."}, status=status.HTTP_400_BAD_REQUEST)