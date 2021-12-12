import os
import requests
from django.views import View
from django.views.generic import FormView
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.core.files.base import ContentFile
from . import forms
from users import models as user_models


class LoginView(View):

    def get(self, request):

        form = forms.LoginForm()

        return render(
            request,
            "users/login.html",
            context={
                "form": form,
            }
        )

    def post(self, request):

        form = forms.LoginForm(request.POST)
        
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                return redirect(reverse("core:home"))

        return render(
            request,
            "users/login.html",
            context={
                "form": form,
            }
        )


def log_out(request):
    logout(request)
    return redirect(reverse("core:home"))


class SignUpView(FormView):
    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        form.save()

        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)

        if user is not None:
            login(self.request, user)

        user.verify_email()
        return super().form_valid(form)


def complete_verification(request, secret):
    try:
        user = user_models.User.objects.get(email_secret=secret)
        user.eamil_verified = True
        user.email_secret = ""
        user.save()
        # todo: add success msg

    except user_models.User.DoesNotExist:
        # Todo : Add error msg
        pass

    return redirect(reverse("core:home"))


def github_login(request):
    client_id = os.environ.get("GITHUB_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/github/callback"

    return redirect(
        f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scrope=read:user"
    )


class GithubException(Exception):
    pass


def github_callback(request):
    try:
        code = request.GET.get("code", None)
        client_id = os.environ.get("GITHUB_ID")
        client_secret = os.environ.get("GITHUB_SECRET")

        if code is not None:

            token_request = requests.post(
                f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}",
                headers={"Accept": "application/json"},
            )

            json_access_token = token_request.json()
            error = json_access_token.get("error", None)

            if error is not None:
                raise GithubException()
            else:
                access_token = json_access_token.get("access_token")
                profile_request = requests.get(
                    "https://api.github.com/user",
                    headers={
                        "Authorization": f"token {access_token}",
                        "Accept": "application/json",
                    },
                )
                profile_json = profile_request.json()
                username = profile_json.get("login", None)

                if username is not None:
                    name = profile_json.get("name")
                    email = profile_json.get("email")
                    bio = profile_json.get("bio")

                    if name is None:
                        name = username

                    if email is None:
                        email = name
                    
                    if bio is None:
                        bio = ""

                    try:
                        user = user_models.User.objects.get(email=email)

                        if user.login_method != user_models.User.LOGIN_GH:
                            raise GithubException()

                    except user_models.User.DoesNotExist:
                        user = user_models.User.objects.create(
                            email=email,
                            first_name=name,
                            bio=bio,
                            username=email,
                            login_method=user_models.User.LOGIN_GH,
                            eamil_verified=True,
                        )
                        user.set_unusable_password()
                        user.save()
                    login(request, user)
                    return redirect(reverse("core:home"))
                        
                else:
                    raise GithubException()
        else:
            return GithubException()
    except GithubException:
        # Todo send error msg
        return redirect(reverse("users:login"))


class KakaoException(Exception):
    pass


def kakao_login(request):
    rest_api_key = os.environ.get("KAKAO_REST_API_KEY")
    callback_url = "http://127.0.0.1:8000/users/login/kakao/callback"
    redirect_uri = f"kauth.kakao.com/oauth/authorize?client_id={rest_api_key}&redirect_uri={callback_url}&response_type=code"
    return redirect(f"https://{redirect_uri}")


def kakao_callback(request):
    try:
        rest_api_key = os.environ.get("KAKAO_REST_API_KEY")
        callback_url = "http://127.0.0.1:8000/users/login/kakao/callback"
        code = request.GET.get("code")
        token_request = requests.get(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={rest_api_key}&redirect_uri={callback_url}&code={code}"
        )

        token_response_json = token_request.json()
        error = token_response_json.get("error", None)

        if error is not None:
            raise KakaoException()

        access_token = token_response_json.get("access_token")
        profile_request = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        profile_json = profile_request.json()
        email = profile_json.get("kakao_account").get("email", None)

        if email is None:
            raise KakaoException()

        properties = profile_json.get("properties")

        nickname = properties.get("nickname")
        gender = profile_json.get("kakao_account").get("gender")
        profile_image = profile_json.get("kakao_account")
        profile_image = profile_image.get("profile").get("profile_image_url")

        print("프로필", profile_image)

        try:
            user = user_models.User.objects.get(email=email)
            if user.login_method != user_models.User.LOGIN_KAKAO:
                raise KakaoException()

        except user_models.User.DoesNotExist:
            user = user_models.User.objects.create(
                email=email,
                username=email,
                first_name=nickname,
                gender=gender,
                login_method=user_models.User.LOGIN_KAKAO,
                eamil_verified=True,
            )
            user.set_unusable_password()
            user.save()
            if profile_image is not None:
                photo_request = requests.get(profile_image)
                user.avatar.save(
                    f"{nickname}-avatar",
                    ContentFile(photo_request.content)
                )
        login(request, user)
        return redirect(reverse("core:home"))

    except KakaoException:
        return redirect(reverse("users:login"))
