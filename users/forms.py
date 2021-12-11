from django import forms
from . import models as user_models


class LoginForm(forms.Form):

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

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
            