from django.shortcuts import render, get_object_or_404
from soccer.models import SoccerField
from soccer.decorators import admin_required
from soccer.forms import SoccerFieldForm
from django.shortcuts import redirect
from soccer.enums import SoccerFieldStatus

def detail(request, pk):
    field = get_object_or_404(SoccerField, pk=pk)
    return render(request, 'soccer/field_detail.html', {'field': field})

@admin_required
def admin_all_fields(request):
    fields = SoccerField.objects.all()
    return render(request, 'soccer/admin_all_fields.html', {'fields': fields, 'soccer_field_status': SoccerFieldStatus})

@admin_required
def admin_field_detail(request, pk):
    field = get_object_or_404(SoccerField, pk=pk)
    return render(request, 'soccer/admin_field_detail.html', {'field': field, 'soccer_field_status': SoccerFieldStatus})

@admin_required
def admin_add_field(request):
    if request.method == "POST":
        form = SoccerFieldForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_all_fields')
    else:
        form = SoccerFieldForm()
    return render(request, 'soccer/admin_field_form.html', {'form': form, 'field': None})

@admin_required
def admin_edit_field(request, pk):
    field = get_object_or_404(SoccerField, pk=pk)
    if request.method == "POST":
        form = SoccerFieldForm(request.POST, request.FILES, instance=field)
        if form.is_valid():
            form.save()
            return redirect('admin_all_fields')
    else:
        form = SoccerFieldForm(instance=field)
    return render(request, 'soccer/admin_field_form.html', {'form': form, 'field': field})
