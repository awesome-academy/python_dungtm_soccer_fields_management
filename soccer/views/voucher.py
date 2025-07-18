from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import gettext as _
from soccer.forms import VoucherForm
from soccer.models import Voucher
from django.contrib.auth.decorators import login_required
from soccer.decorators import admin_required
from django.utils import timezone
from django.db.models import Q
from soccer.constants import DATE_FORMAT
from django.http import JsonResponse
from django.utils.dateparse import parse_datetime

@login_required
def voucher_list_user(request):
    now = timezone.now()
    vouchers = Voucher.objects.filter(
        valid_from__lte=now,
        valid_to__gte=now
    ).filter(
        Q(deleted_at__isnull=True) | Q(deleted_at__gt=now)
    ).filter(
        rest_quantity__gt=0
    ).order_by('-valid_to')
    return render(request, "soccer/voucher_list_user.html", {"vouchers": vouchers, "now": timezone.now(), "DATE_FORMAT": DATE_FORMAT})

@admin_required
def voucher_list_admin(request):
    vouchers = Voucher.objects.all().order_by('-valid_to')
    return render(request, "soccer/voucher_list_admin.html", {"vouchers": vouchers, "now": timezone.now(), "DATE_FORMAT": DATE_FORMAT})

@admin_required
def voucher_create(request):
    if request.method == "POST":
        form = VoucherForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("voucher_list")
    else:
        form = VoucherForm()
    return render(request, "soccer/voucher_form.html", {"form": form, "title": _("Add Voucher")})

@admin_required
def voucher_edit(request, pk):
    voucher = get_object_or_404(Voucher, pk=pk)
    if request.method == "POST":
        form = VoucherForm(request.POST, instance=voucher)
        if form.is_valid():
            form.save()
            return redirect("voucher_list")
    else:
        form = VoucherForm(instance=voucher)
    return render(request, "soccer/voucher_form.html", {"form": form, "title": _("Edit Voucher"), "voucher": voucher})

@admin_required
def voucher_delete(request, pk):
    voucher = get_object_or_404(Voucher, pk=pk)
    if voucher.deleted_at is not None and voucher.deleted_at <= timezone.now():
        return render(request, "soccer/voucher_delete.html", {
            "voucher": voucher,
            "error": _("Voucher already deleted."),
            "now": timezone.now()
        })
    if request.method == "POST":
        deleted_at = request.POST.get("deleted_at")
        if deleted_at:
            try:
                dt = parse_datetime(deleted_at)
                if not dt:
                    raise ValueError
                voucher.deleted_at = dt
                voucher.save()
                return redirect("voucher_list_admin")
            except Exception:
                return render(request, "soccer/voucher_delete.html", {
                    "voucher": voucher,
                    "error": _("Invalid date/time."),
                    "now": timezone.now()
                })
        else:
            return render(request, "soccer/voucher_delete.html", {
                "voucher": voucher,
                "error": _("Delete time required."),
                "now": timezone.now()
            })
    return render(request, "soccer/voucher_delete.html", {
        "voucher": voucher,
        "now": timezone.now()
    })