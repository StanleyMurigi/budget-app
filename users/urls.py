# from django.urls import path
# from rest_framework_simplejwt.views import TokenRefreshView
# from .views import RegisterView, CustomTokenObtainPairView

# urlpatterns = [
#     path('register/', RegisterView.as_view(), name='register'),
#     path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
#     path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
# ]

from django.urls import path
from .views import user_login, user_register, user_logout

urlpatterns = [
    path('login/', user_login, name='login'),
    path('register/', user_register, name='register'),
    path('logout/', user_logout, name='logout'),
]
