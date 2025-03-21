# from rest_framework import generics
# from django.contrib.auth import get_user_model
# from rest_framework.permissions import AllowAny
# from rest_framework_simplejwt.views import TokenObtainPairView
# from .serializers import CustomUserSerializer, CustomTokenObtainPairSerializer

# User = get_user_model()

# class RegisterView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = CustomUserSerializer
#     permission_classes = [AllowAny]

# class CustomTokenObtainPairView(TokenObtainPairView):
#     serializer_class = CustomTokenObtainPairSerializer

# filepath: /home/mahihu/Workspace/budget-app/users/views.py
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomAuthenticationForm

def user_login(request):
    """Login view using custom authentication form."""
    if request.method == "POST":
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')  # Redirect to budget dashboard
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'users/login.html', {'form': form})

def user_register(request):
    """User registration view."""
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto-login after registration
            return redirect('index')  # Redirect to home page
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'users/register.html', {'form': form})

def user_logout(request):
    """Logout view."""
    logout(request)
    return redirect('login')
