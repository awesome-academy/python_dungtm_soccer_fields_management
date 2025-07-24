from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils.translation import gettext as _
from soccer.decorators import admin_required
from soccer.models import FieldRequest, RequestStatus, SoccerFieldStatus
from soccer.forms import FieldRequestForm
from soccer.constants import PAGINATION_LIMIT, PAGINATION_PAGE, PAGINATION_LIMITS, DATE_TIME_FORMAT
from soccer.enums import RequestType
from django.db import transaction
from soccer.models import SoccerField
from django.utils import timezone

@login_required
def create_field_request(request):
    print(request.method)
    if request.method == "POST":
        form = FieldRequestForm(request.POST or None, request.FILES or None)
        print(form)
        if form.is_valid():
            fr = form.save(commit=False)
            fr.user = request.user
            fr.save()
            return redirect('my_field_requests')
    else:
        form = FieldRequestForm()
        print(form)
    return render(request, 'soccer/field_request_form.html', {'form': form})

@login_required
def edit_field_request(request, pk):
    fr = get_object_or_404(FieldRequest, pk=pk, user=request.user, status=RequestStatus.PENDING)
    if request.method == "POST":
        form = FieldRequestForm(request.POST, request.FILES, instance=fr)
        if form.is_valid():
            form.save()
            return redirect('my_field_requests')
    else:
        form = FieldRequestForm(instance=fr)
    return render(request, 'soccer/field_request_form.html', {'form': form, 'edit': True})

@login_required
def my_field_requests(request):
    requests = FieldRequest.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'soccer/my_field_requests.html', {'requests': requests, 'DATE_TIME_FORMAT': DATE_TIME_FORMAT})

@login_required
def field_request_detail(request, pk):
    field_request = get_object_or_404(FieldRequest, pk=pk)
    if field_request.user != request.user:
        return render(request, 'soccer/403.html', status=403)
    return render(request, 'soccer/field_request_detail.html', {'fr': field_request, 'DATE_TIME_FORMAT': DATE_TIME_FORMAT, 'request_status': RequestStatus})

@admin_required
def admin_field_request_detail(request, pk):
    field_request = get_object_or_404(FieldRequest, pk=pk)
    return render(request, 'soccer/admin_field_request_detail.html', {'fr': field_request})

@admin_required
def admin_field_requests(request):
    searchtext = request.GET.get('searchtext', '')
    page = int(request.GET.get('page', PAGINATION_PAGE))
    limit = int(request.GET.get('limit', PAGINATION_LIMIT))
    qs = FieldRequest.objects.all()
    if searchtext:
        qs = qs.filter(Q(note__icontains=searchtext) | Q(user__username__icontains=searchtext))
    qs = qs.order_by('-created_at')
    paginator = Paginator(qs, limit)
    requests = paginator.get_page(page)
    return render(request, 'soccer/admin_field_requests.html', {
        'requests': requests,
        'searchtext': searchtext,
        'limit': limit,
        'limits': PAGINATION_LIMITS,
        'DATE_TIME_FORMAT': DATE_TIME_FORMAT,
    })

@admin_required
def admin_update_field_request_status(request, pk):
    fr = get_object_or_404(FieldRequest, pk=pk)
    action = request.POST.get('action')

    if action == 'approve':
        with transaction.atomic():
            if fr.type == RequestType.ADD:
                SoccerField.objects.create(
                    name=fr.name,
                    address=fr.address,
                    phone=fr.phone,
                    email=fr.email,
                    type=fr.type_field,
                    image=fr.image,
                    price_per_hour=fr.price_per_hour,
                    description=fr.description,
                )

            elif fr.type == RequestType.UPDATE and fr.soccer_field:
                field = fr.soccer_field
                field.name = fr.name
                field.address = fr.address
                field.phone = fr.phone
                field.email = fr.email
                field.type = fr.type_field
                field.price_per_hour = fr.price_per_hour
                field.description = fr.description
                if fr.image:
                    field.image = fr.image
                field.save()

            elif fr.type == RequestType.DELETE and fr.soccer_field:
                field = fr.soccer_field
                field.status = SoccerFieldStatus.INACTIVE
                field.deleted_at = timezone.now()
                field.save()

            fr.status = RequestStatus.APPROVED
            fr.save()

    elif action == 'reject':
        fr.status = RequestStatus.REJECTED
        fr.save()

    return redirect('admin_field_requests')

@login_required
def cancel_field_request(request, pk):
    fr = get_object_or_404(FieldRequest, pk=pk, user=request.user, status=RequestStatus.PENDING)
    if request.method == 'POST':
        fr.status = RequestStatus.CANCELLED
        fr.save()
        return redirect('my_field_requests')
    return render(request, 'soccer/cancel_field_request.html', {'fr': fr})
