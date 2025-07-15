from django.shortcuts import redirect, get_object_or_404, render
from soccer.utils import send_activation_email
from soccer.forms import CustomUserCreationForm, OrderFieldForm
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from .models import SoccerField, Order, Voucher
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from soccer.enums import OrderStatus
from decimal import Decimal
from datetime import timedelta
from django.utils.translation import gettext as _
from django.db import transaction

# Create your views here.
def register(request):
    if request.user.is_authenticated:
        pass
        # return redirect('soccer_home')
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False 
            user.save()
            send_activation_email(request, user) 
            return render(request, "registration/register_done.html", {"email": user.email})
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/register.html", {"form": form})

def home(request):
    if not request.user.is_authenticated:
        return redirect('register')
    return render(request, "soccer/home.html", {"user": request.user})

def activate_account(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, "activation/activation_success.html")
    else:
        return render(request, "activation/activation_invalid.html")
    
def home(request):
    name_query = request.GET.get('name', '')
    type_query = request.GET.get('type', '')
    soccer_fields = SoccerField.objects.all()
    
    if name_query:
        soccer_fields = soccer_fields.filter(name__icontains=name_query)
    if type_query:
        soccer_fields = soccer_fields.filter(type=type_query)
    
    field_types = SoccerField.objects.values_list('type', flat=True).distinct()

    page_number = request.GET.get('page')
    paginator = Paginator(soccer_fields, 9) 
    page_obj = paginator.get_page(page_number)

    return render(request, 'soccer/home.html', {
        'soccer_fields': page_obj.object_list,
        'page_obj': page_obj,
        'name_query': name_query,
        'type_query': type_query,
        'field_types': field_types,
    })

def detail(request, pk):
    field = get_object_or_404(SoccerField, pk=pk)
    return render(request, 'soccer/field_detail.html', {'field': field})

@login_required
def order_field(request, pk):
    field = get_object_or_404(SoccerField, pk=pk)
    vouchers = Voucher.objects.filter(rest_quantity__gt=0)
    error_message = None

    if request.method == 'POST':
        form = OrderFieldForm(request.POST)
        if form.is_valid():
            time = form.cleaned_data['time']
            duration = form.cleaned_data['duration']
            end_time = time + timedelta(minutes=duration)

            overlap_orders = Order.objects.filter(
                soccer_field=field,
                status__in=[OrderStatus.PENDING, OrderStatus.CONFIRMED, OrderStatus.COMPLETED],
                time__lt=end_time
            )

            overlap_exists = False
            for order in overlap_orders:
                order_end_time = order.time + timedelta(minutes=order.duration)
                if order_end_time > time:
                    overlap_exists = True
                    break

            if overlap_exists:
                error_message = _("This time slot has already been booked. Please select another time.")
            else:
                with transaction.atomic():
                    order = form.save(commit=False)
                    order.user = request.user
                    order.soccer_field = field
                    order.status = OrderStatus.PENDING
                    order.save()
                    if order.voucher:
                        order.voucher.rest_quantity = max(0, order.voucher.rest_quantity - 1)
                        order.voucher.save()
                return redirect('order_detail', pk=order.pk)
    else:
        form = OrderFieldForm()

    return render(request, 'soccer/order_field.html', {
        'form': form,
        'field': field,
        'vouchers': vouchers,
        'error_message': error_message,
        'total_price': None,
    })

@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if order.user != request.user:
        return render(request, '403.html', status=403)
    base_price = order.soccer_field.price_per_hour * (Decimal(order.duration) / Decimal(60))
    discount = 0
    if order.voucher:
        if base_price >= order.voucher.min_price:
            discount = base_price * order.voucher.discount_percent / 100
            if discount > order.voucher.max_discount_amount:
                discount = order.voucher.max_discount_amount
    total_price = max(0, base_price - discount)
    return render(request, 'soccer/order_detail.html', {'order': order, 'total_price': total_price})