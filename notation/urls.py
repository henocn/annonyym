
from django.contrib import admin
from django.urls import path, include
from main.views import ObtainAuthTokenView, ChangePasswordView, RegisterView
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('messages/', include('main.urls')),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/token/', ObtainAuthTokenView.as_view(), name='auth_token'),
    path('auth/change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('auth/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]
