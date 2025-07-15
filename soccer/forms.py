from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from soccer.models import Order, Voucher

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.is_active = False
            user.save()
        return user
    
class OrderFieldForm(forms.ModelForm):
    time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        label=_("Order Time")
    )
    note = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        required=False,
        label=_("Note")
    )

    class Meta:
        model = Order
        fields = ['time', 'duration', 'note', 'voucher']
        widgets = {
            'time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'duration': forms.Select(attrs={'class': 'form-control'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'voucher': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['voucher'].queryset = Voucher.objects.filter(rest_quantity__gt=0)
        self.fields['voucher'].required = False
        self.fields['voucher'].widget.attrs.update({'class': 'form-control'})