from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic.base import View
from .models import USER_ROLES, UserProfile


class HomeView(View):
    def get(self, request):
        context = {

        }
        return render(request, 'home.html', context)


class RegistrationView(View):
    def get(self, request):
        context = dict()
        return render(request, 'users_auth/user_register.html', context)

    def post(self, request):
        data = request.POST
        first_name = data.get('firstname')
        last_name = data.get('lastname')
        email = data.get('email')
        password = data.get('password')
        about = data.get('about')
        image = request.FILES.get('image')
        is_admin = data.get('is_admin')
        status = data.get('status')

        email_taken = User.objects.filter(username=email).exists()
        if email_taken:
            messages.info(request, "This email is already taken. ")
            return redirect('users_auth:registration')
        else:
            user_obj = User.objects.create_user(username=email,  first_name=first_name, last_name=last_name,
                                                password=password, email=email)
            user_obj.save()

            user_profile = UserProfile.objects.get(user=user_obj)
            user_profile.role = is_admin
            user_profile.is_active = True if status == '1' else False
            user_profile.details = about

            if image:
                user_profile.image = image

            user_profile.save()

        return redirect('users_auth:users_list')


class UserList(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        profiles = UserProfile.objects.filter(is_active=True)

        context = {
            'profiles': profiles
        }

        return render(request, 'users_auth/users_list.html', context)


class UpdateUser(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, profile_id):
        profile_obj = UserProfile.objects.get(id=profile_id)

        context = {
            'object': profile_obj,
        }
        return render(request, 'users_auth/update_user.html', context)

    def post(self, request, profile_id):
        data = request.POST

        profile_obj = UserProfile.objects.get(id=profile_id)

        first_name = data.get('firstname')
        last_name = data.get('lastname')
        email = data.get('email')
        password = data.get('password')
        about = data.get('about')
        image = request.FILES.get('image')
        is_admin = data.get('is_admin')
        status = data.get('status')

        email_exists = ''
        if profile_obj.user.email != email:
            email_exists = User.objects.filter(email=email)

        if email_exists:
            messages.info(request, 'Email Address already Taken. ')
        else:
            user_obj = profile_obj.user
            user_obj.email = email
            user_obj.first_name = first_name
            user_obj.last_name = last_name

            if password:
                user_obj.password = password
            user_obj.save()

        if image:
            profile_obj.image = image

        profile_obj.role = is_admin
        profile_obj.is_active = True if status == '1' else False
        profile_obj.save()

        messages.success(request, 'User Profile Updated Successfully. ')
        return redirect('users_auth:update_user', profile_id=profile_id)


class RemoveUser(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, profile_id):
        profile_obj = UserProfile.objects.get(id=profile_id)
        profile_obj.is_active = False
        profile_obj.save()

        messages.success(request, "User Removed Successfully. ")
        return redirect('users_auth:users_list')


class UserLogin(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        context = dict()
        return render(request, 'users_auth/login.html', context)

    def post(self, request):
        data = request.POST

        username = data.get('username')
        password = data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('users_auth:home_url')
        else:
            messages.info(request, 'Username or Password is Incorrect!')
        return redirect('users_auth:login_url')


class SignOut(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        logout(request)
        return redirect('users_auth:login_url')
