from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render,redirect
from django.views import View
from accounts.forms import UserForm,LoginForm,ProfileForm
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from accounts.forms import OtpLoginForm
from accounts.models import EmailOTP,Profile
from django.core.mail import send_mail

from listing.models import Property, Enquiry
from django.contrib.auth.decorators import login_required
from accounts.models import Contact


# Create your views here.
#admin-page:
def is_admin(user):
    return user.is_superuser
@method_decorator(user_passes_test(is_admin), name='dispatch')
class AdminDashboardView(View):
    def get(self, request):
        agent_count=Profile.objects.filter(role='agent').count()
        buyer_count = Profile.objects.filter(role='buyer').count()
        pendingenquiry_count = Enquiry.objects.filter(status='pending').count()
        context = {
            'properties': Property.objects.all(),
            'enquiries': Enquiry.objects.all(),
            'users': Profile.objects.all(),
            'agent_count': agent_count,
            'buyer_count': buyer_count,
            'pendingenquiry_count': pendingenquiry_count,
        }
        return render(request,'admin/admin_dashboard.html',context)

class PropertyManagementView(View):
    def get(self, request):
        property_list = Property.objects.all()
        context = {'properties': property_list}
        return render(request,'admin/property_management.html',context)
@method_decorator(user_passes_test(is_admin), name='dispatch')
class AgentmanagementView(View):
    def get(self, request):
        agents=Profile.objects.filter(role='agent')
        context={'agents': agents}
        return render(request,'admin/agent_management.html',context)

@method_decorator(user_passes_test(is_admin), name='dispatch')
class ToggleAgentView(View):
    def get(self, request,pk):
        agent =Profile.objects.get(pk=pk, role='agent')
        active = request.GET.get('active')
        if active == '1':
            agent.user.is_active = True
        else:
            agent.user.is_active = False

        agent.user.save()
        return redirect('accounts:agentmanagement')

@method_decorator(user_passes_test(is_admin), name='dispatch')
class BuyermanagementView(View):
    def get(self, request):
        buyers=Profile.objects.filter(role='buyer')
        context={'buyers': buyers}
        return render(request,'admin/buyer_management.html',context)

@method_decorator(user_passes_test(is_admin), name='dispatch')
class ToggleBuyerView(View):
    def get(self, request,i):
        buyer=Profile.objects.get(id=i, role='buyer')
        active= request.GET.get('active')
        if active == '1':
            buyer.user.is_active = True
        else:
            buyer.user.is_active = False

        buyer.user.save()
        return redirect('accounts:buyermanagement')

class EnquiryManagementView(View):
    def get(self, request):
        enquiries=Enquiry.objects.all()
        context={'enquiries': enquiries}
        return render(request,'admin/enquiry_management.html',context)

class MessagesManagementView(View):
    def get(self, request):
        c=Contact.objects.all()
        context={'messages': c}
        return render(request,'admin/messages_management.html',context)
#admin-page/>


class Registerview(View):
    def get(self, request):
        user_form = UserForm()
        profile_form = ProfileForm()
        context = {'registerform': user_form, 'profileform': profile_form}
        return render(request,'register.html',context)
    def post(self, request):
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST,request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            print(user)
            profile = user.profile
            profile.phone = profile_form.cleaned_data['phone']
            profile.address = profile_form.cleaned_data['address']
            profile.profile_picture = profile_form.cleaned_data['profile_picture']
            profile.save()
            print(profile)
            return redirect('accounts:login')
        else:
            messages.error(request, "error, check your username and password")
            context = {'registerform': user_form, 'profileform': profile_form}
            return render(request,'register.html',context)

class Loginview(View):
    def get(self, request):
        form_instance = LoginForm()
        context = {'loginform': form_instance}
        return render(request,'login.html',context)
    def post(self, request):
        form_instance = LoginForm(request.POST)
        if form_instance.is_valid():
            data=form_instance.cleaned_data #fetches data after validation
            u=data['username']#retrieves username from cleaned data
            p=data['password']#retrieves username from cleaned data
            user=authenticate(username=u,password=p)#calls authenticate to verify if user exists
                                                    #if user exists then it returns to the user object
                                                    #else none
            if user and user.is_superuser == True:#if user is admin
                login(request, user)
                print('admin logged in')
                return redirect('accounts:admin_dashboard')
            elif user and user.is_superuser != True:#if user is not admin and exists
                login(request,user)  #add the user into current session
                return redirect('index')
            else: #if not exists
                messages.error(request, "Invalid Username or Password!")
                return redirect('accounts:login')

class LoginViaOtp(View):
    def get(self, request):
        form_instance = OtpLoginForm()
        context = {'otpform': form_instance}
        return render(request,'loginviaotp.html',context)
    def post(self, request):
        form_instance = OtpLoginForm(request.POST)
        if form_instance.is_valid():
            u=form_instance.save(commit=False)
            u.generate_otp()
            send_mail(
                subject="Landonhand-OTP",
                message=f"Dear {u.user.username},\n\n"
                        f"Your OTP for LandOnHand Login is {u.code}.\n\n\n"
                        f"Do Not share the OTP with anyone including Landonhand personal.",
                from_email=None,
                recipient_list=[u.user.email],
                fail_silently=False,
            )
            u.save()
            e=u.user.email
            me=e[0:2]+'******'+e[-9:]
            messages.success(request,f'Email has been sent to {me} successfully!')
            return redirect('accounts:otpverification')

class OtpVerificationView(View):
    def get(self, request):
        return render(request,'otpverification.html')
    def post(self, request):
        o = request.POST['o']  # retrieve the otp send by the user
        try:
            u = EmailOTP.objects.get(code=o)  # check whether record matching with the entered otp exists
        except EmailOTP.DoesNotExist:
            messages.error(request, "Invalid or expired OTP!")
            return redirect('accounts:otpverification')
        #checks expiry of otp:
        if not u.is_valid():
            u.delete()  # remove expired OTP
            messages.error(request, "OTP has expired. Please request a new one.")
            return redirect('accounts:loginviaotp')

        # if exists then:
        # u.code = None  # clear the otp from table
        user=u.user
        u.delete() #clear the entire emailotp field
        login(request,user)  # add the user into current session
        return redirect('index')



class Logoutview(View):
    def get(self, request):
        logout(request)
        return redirect('accounts:login')

@method_decorator(login_required, name='dispatch')
class ContactUsView(View):
    def get(self, request):
        return render(request,'contact.html')
    def post(self, request):
        name=request.POST['name']
        email=request.POST['email']
        sub=request.POST['sub']
        msg=request.POST['msg']
        e=Contact.objects.create(user=request.user,name=name,email=email,subject=sub,message=msg)
        e.save()
        send_mail(
            subject=f"{e.subject}",  # f-string ensures it's a string
            message=f"{e.message}",  # same here
            from_email=e.user.email,  # pass directly, no {}
            recipient_list=['landonhand3@gmail.com'],
            fail_silently=False,
        )
        return redirect('index')

