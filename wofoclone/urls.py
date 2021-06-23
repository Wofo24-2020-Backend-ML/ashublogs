
from django.contrib import admin
from django.urls import path
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', views.UserAPIVIEW.as_view()),
    path('user/<int:pk>', views.UserAPIVIEW.as_view()),
    path('createuser/', views.UserSignupAPIVIEW.as_view()),
    path('login/', views.LoginView.as_view()),
    path('activate/<user_id>', views.ActivateView.as_view()),
]
