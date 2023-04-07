from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(
        attrs={'class': 'form-control form-control-lg', 'placeholder': '用户名'}))
    password = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(
        attrs={'class': 'form-control form-control-lg', 'placeholder': '密码'}))


class RegisterForm(forms.Form):
    a = (('男', '男'), ('女', '女'))

    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(
        attrs={'id': 'username', 'type': 'text', 'placeholder': '请输入用户名'}))
    password = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(
        attrs={'class': 'form-control form-control-lg', 'placeholder': '密码'}))
    password2 = forms.CharField(label="确认密码", max_length=256, widget=forms.PasswordInput(
        attrs={'class': 'form-control form-control-lg', 'placeholder': '确认密码'}))
    phone = forms.CharField(label='电话', widget=forms.TextInput(
        attrs={'class': 'form-control form-control-lg', 'placeholder': '手机'}))
    email = forms.EmailField(label='邮箱', widget=forms.TextInput(
        attrs={'class': 'form-control form-control-lg', 'placeholder': '邮箱'}))
    sex = forms.ChoiceField(label='性别', choices=a, widget=forms.Select(
        attrs={"class": "custom-select custom-select-lg mb-3"}))  # choices 设置元组值
