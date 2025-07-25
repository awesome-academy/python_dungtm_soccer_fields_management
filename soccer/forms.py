from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from soccer.models import Order, Voucher, FieldRequest
from soccer.constants import MAX_LENGTH_1000, MIN_VALUE_1, MAX_VALUE_5, MAX_LENGTH_128, MAX_LENGTH_256, MAX_LENGTH_32

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

class VoucherForm(forms.ModelForm):
    class Meta:
        model = Voucher
        fields = ["code", "description", "discount_percent", "valid_from", "valid_to", "min_price", "max_discount_amount", "rest_quantity"]
        widgets = {
            'valid_from': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'valid_to': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }

class ReviewForm(forms.Form):
    rate = forms.IntegerField(min_value=MIN_VALUE_1, max_value=MAX_VALUE_5, label=_("Rate"),)
    comment = forms.CharField(widget=forms.Textarea, label=_("Comment"), max_length=MAX_LENGTH_1000, required=False)

class FieldRequestForm(forms.ModelForm):
    class Meta:
        model = FieldRequest
        fields = [
            'type', 'soccer_field', 'name', 'address', 'phone', 'email',
            'type_field', 'price_per_hour', 'image', 'description', 'note'
        ]
        widgets = {
            'type': forms.Select(attrs={'class': 'form-select'}),
            'soccer_field': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'maxlength': MAX_LENGTH_128}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'maxlength': MAX_LENGTH_256}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'maxlength': MAX_LENGTH_32}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'type_field': forms.Select(attrs={'class': 'form-select'}),
            'price_per_hour': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'note': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        type = cleaned_data.get("type")
        soccer_field = cleaned_data.get("soccer_field")

        if type in ['update', 'delete'] and not soccer_field:
            self.add_error("soccer_field", _("This field is required."))
        elif type == 'add':
            cleaned_data["soccer_field"] = None

        return cleaned_data
    