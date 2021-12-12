from django import forms
from django.forms import widgets
from . import models as user_models


class LoginForm(forms.Form):

    email = forms.EmailField(label="이메일")
    password = forms.CharField(widget=forms.PasswordInput, label="비밀번호")

# 데이터 필드를 확인하고 싶으면 메서드 이름앞에 clean_을 넣어야 한다.
# clean으로 시작하는 메서드는 에러를 넣는 것뿐만 아니라 데이터도 정리해준다.
# clean으로 시작하는 메서드는 Return을 하지 않으면 해당 데이터 필드를 지워버린다.(기억하지 않는다)

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            user = user_models.User.objects.get(email=email)
            if user.check_password(password):
                return self.cleaned_data
            else:
                self.add_error("password", forms.ValidationError("비밀번호가 일치하지 않습니다."))
        except user_models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("존재하지않는 사용자입니다."))


class SignUpForm(forms.Form):

    email = forms.EmailField(max_length=255, label="이메일")
    first_name = forms.CharField(max_length=10, label="닉네임")
    password = forms.CharField(widget=forms.PasswordInput, label="비밀번호")
    password1 = forms.CharField(widget=forms.PasswordInput, label="비밀번호 확인")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            user_models.User.objects.get(email=email)
            raise forms.ValidationError("이미 존재하는 사용자입니다.")
        except user_models.User.DoesNotExist:
            return email

    def clean_password1(self):
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")

        if password != password1:
            raise forms.ValidationError("비밀번호가 일치하지 않습니다.")
        else:
            return password

    def save(self):     
        first_name = self.cleaned_data.get("first_name")
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user = user_models.User.objects.create_user(email, email, password)
        user.first_name = first_name
        user.save()