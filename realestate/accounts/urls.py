from django.urls import path
from accounts.views import Loginview,Registerview, Logoutview


app_name = 'accounts'
urlpatterns = [
    path('login/', Loginview.as_view(), name='login'),
    path('register/', Registerview.as_view(), name='register'),
    path('logout/', Logoutview.as_view(), name='logout'),
]