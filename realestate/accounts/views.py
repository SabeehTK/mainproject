from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render,redirect
from django.views import View
from accounts.forms import UserForm,LoginForm,ProfileForm
from django.contrib import messages



# Create your views here.
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
            if user:#if user exists
                login(request,user)  #add the user into current session
                return redirect('index')
            else: #if not exists
                messages.error(request, "Invalid Username or Password!")
                return redirect('accounts:login')

class Logoutview(View):
    def get(self, request):
        logout(request)
        return redirect('accounts:login')