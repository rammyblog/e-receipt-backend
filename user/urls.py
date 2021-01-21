from django.urls import path

from user.views import CustomTokenObtainPairView, CustomTokenRefreshView

urlpatterns = [
    path('jwt/token/create', CustomTokenObtainPairView.as_view()),
    path('jwt/token/refresh', CustomTokenRefreshView.as_view()),
]
