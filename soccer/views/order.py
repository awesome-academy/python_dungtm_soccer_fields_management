from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from soccer.forms import OrderFieldForm
from soccer.models import SoccerField, Order, Voucher
from soccer.enums import OrderStatus
from decimal import Decimal
from datetime import timedelta
from django.utils.translation import gettext as _
from django.db import transaction
from soccer.constants import DATE_FORMAT

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
        'DATE_FORMAT': DATE_FORMAT
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