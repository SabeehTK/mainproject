from django.urls import path
from accounts.views import Loginview,Registerview, Logoutview
from accounts.views import OtpVerificationView, LoginViaOtp
from accounts.views import AdminDashboardView
from accounts.views import AgentmanagementView
from accounts.views import ToggleAgentView
from accounts.views import PropertyManagementView
from accounts.views import BuyermanagementView
from accounts.views import ToggleBuyerView
from accounts.views import EnquiryManagementView
from accounts.views import ContactUsView
from accounts.views import MessagesManagementView

app_name = 'accounts'
urlpatterns = [
    path('login/', Loginview.as_view(), name='login'),
    path('loginviaotp/', LoginViaOtp.as_view(), name='loginviaotp'),
    path('otpverification/', OtpVerificationView.as_view(), name='otpverification'),
    path('register/', Registerview.as_view(), name='register'),
    path('logout/', Logoutview.as_view(), name='logout'),
    path('contact/', ContactUsView.as_view(), name='contact'),
    #admin page urls:-
    path('admin-dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('propertymanagement/',PropertyManagementView.as_view(), name='propertymanagement'),
    path('agentmanagement/',AgentmanagementView.as_view(), name='agentmanagement'),
    path('toggleagent/<int:pk>',ToggleAgentView.as_view(), name='toggleagent'),
    path('buyermanagement/',BuyermanagementView.as_view(), name='buyermanagement'),
    path('togglebuyer/<int:i>',ToggleBuyerView.as_view(), name='togglebuyer'),
    path('enquirymanagement/',EnquiryManagementView.as_view(), name='enquirymanagement'),
    path('messagesmanagement/',MessagesManagementView.as_view(), name='messagesmanagement'),
]