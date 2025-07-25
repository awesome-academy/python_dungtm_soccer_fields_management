from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from soccer.forms import OrderFieldForm, ReviewForm
from soccer.models import SoccerField, Order, Voucher, Review
from soccer.enums import OrderStatus
from decimal import Decimal
from datetime import timedelta
from django.utils.translation import gettext as _
from django.db import transaction
from soccer.constants import DATE_FORMAT, DATE_TIME_FORMAT, TIME_FORMAT
from soccer.decorators import admin_required
from django.http import JsonResponse
from soccer.utils import user_can_review_field
from soccer.utils import user_can_review_field

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
        return render(request, 'soccer/403.html', status=403)
    base_price = order.soccer_field.price_per_hour * (Decimal(order.duration) / Decimal(60))
    review = Review.objects.filter(user=request.user, soccer_field=order.soccer_field).first()
    review = Review.objects.filter(user=request.user, soccer_field=order.soccer_field).first()
    discount = 0
    if order.voucher:
        if base_price >= order.voucher.min_price:
            discount = base_price * order.voucher.discount_percent / 100
            if discount > order.voucher.max_discount_amount:
                discount = order.voucher.max_discount_amount
    total_price = max(0, base_price - discount)
    return render(request, 'soccer/order_detail.html', {
        "order": order,
        "total_price": total_price,
        "review": review,
        "all_statuses": OrderStatus,
    })

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-time')
    return render(request, 'soccer/my_orders.html', {'orders': orders, 'OrderStatus': OrderStatus})

@login_required
def order_edit(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    if order.status != OrderStatus.PENDING:
        return render(request, 'soccer/403.html', status=403)
    if request.method == "POST":
        form = OrderFieldForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('order_detail', pk=order.pk)
    else:
        form = OrderFieldForm(instance=order)
    return render(request, "soccer/order_field.html", {
        "form": form,
        "field": order.soccer_field,
        "vouchers": Voucher.objects.filter(rest_quantity__gt=0),
        "error_message": None,
        "total_price": None,
        "DATE_FORMAT": DATE_FORMAT,
        "edit_mode": True
    })

@login_required
def order_cancel(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    error_message = None

    if order.status != OrderStatus.PENDING:
        error_message = _('You cannot cancel this order because it has already been processed or cancelled.')
        return render(request, "soccer/order_cancel_confirm.html", {
            "order": order,
            "error_message": error_message,
        })

    if request.method == 'POST':
        cancel_reason = request.POST.get('cancel_reason', '').strip()
        if not cancel_reason:
            error_message = _('Please provide a reason for cancellation.')
        else:
            order.status = OrderStatus.CANCELLED_BY_USER
            order.cancel_reason = cancel_reason
            order.save()
            if order.voucher:
                order.voucher.rest_quantity += 1
                order.voucher.save()
            return redirect('my_orders')

    return render(request, "soccer/order_cancel_confirm.html", {
        "order": order,
        "error_message": error_message,
    })


@admin_required
def admin_cancel_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    error_message = None

    if order.status != OrderStatus.PENDING:
        error_message = _('This order cannot be cancelled because it has already been processed or cancelled.')
        return render(request, "soccer/admin_cancel_order_confirm.html", {
            "order": order,
            "error_message": error_message,
            "DATE_TIME_FORMAT": DATE_TIME_FORMAT
        })

    if request.method == 'POST':
        cancel_reason = request.POST.get('cancel_reason', '').strip()
        if not cancel_reason:
            error_message = _('Please provide a reason for cancellation.')
        else:
            order.status = OrderStatus.CANCELLED_BY_ADMIN
            order.cancel_reason = cancel_reason
            order.save()
            if order.voucher:
                order.voucher.rest_quantity += 1
                order.voucher.save()
            return redirect('all_orders')

    return render(request, "soccer/admin_cancel_order_confirm.html", {
        "order": order,
        "error_message": error_message,
        "DATE_TIME_FORMAT": DATE_TIME_FORMAT
    })

@admin_required
def all_orders(request):
    orders = Order.objects.all().select_related('user', 'soccer_field', 'voucher').order_by('-time')
    return render(request, 'soccer/all_orders.html', {
        'orders': orders,
        'OrderStatus': OrderStatus,
        'DATE_FORMAT': DATE_FORMAT,
        'TIME_FORMAT': TIME_FORMAT
    })

@admin_required
def admin_order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'soccer/admin_order_detail.html', {
        'order': order,
        'total_price': None,
        'DATE_FORMAT': DATE_FORMAT,
        'TIME_FORMAT': TIME_FORMAT
    })

@admin_required
def admin_accept_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == "POST" and request.headers.get("x-requested-with") == "XMLHttpRequest":
        if order.status != OrderStatus.PENDING:
            return JsonResponse({"success": False, "error": _("Order is not pending.")})
        order.status = OrderStatus.CONFIRMED
        order.save()
        return JsonResponse({
            "success": True,
            "new_status": order.status,
            "new_status_display": order.get_status_display(),
        })
    return JsonResponse({"success": False, "error": _("Invalid request.")})

def render_no_permission_review(request, soccer_field, edit=False):
    ctx = {
        "soccer_field": soccer_field,
        "form": None,
        "error": _("You have not completed any orders for this field."),
    }
    if edit:
        ctx["edit"] = True
    return render(request, "soccer/review_field.html", ctx)

@login_required
def review_field(request, pk):
    soccer_field = get_object_or_404(SoccerField, pk=pk)
    if not user_can_review_field(request.user, soccer_field):
        return render_no_permission_review(request, soccer_field)

    try:
        review = Review.objects.get(user=request.user, soccer_field=soccer_field)
        return redirect('edit_review', pk=pk)
    except Review.DoesNotExist:
        pass

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            Review.objects.create(
                soccer_field=soccer_field,
                user=request.user,
                rate=form.cleaned_data["rate"],
                comment=form.cleaned_data["comment"]
            )
            return redirect('soccer_field_detail', pk=soccer_field.pk)
    else:
        form = ReviewForm()

    return render(request, "soccer/review_field.html", {
        "soccer_field": soccer_field,
        "form": form,
    })

@login_required
def edit_review(request, pk):
    soccer_field = get_object_or_404(SoccerField, pk=pk)
    if not user_can_review_field(request.user, soccer_field):
        return render_no_permission_review(request, soccer_field, edit=True)

    review = get_object_or_404(Review, user=request.user, soccer_field=soccer_field)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review.rate = form.cleaned_data["rate"]
            review.comment = form.cleaned_data["comment"]
            review.save()
            return redirect('soccer_field_detail', pk=soccer_field.pk)
    else:
        form = ReviewForm(initial={
            "rate": review.rate,
            "comment": review.comment,
        })

    return render(request, "soccer/review_field.html", {
        "soccer_field": soccer_field,
        "form": form,
        "edit": True,
    })
