from django.shortcuts import render, get_object_or_404
from soccer.models import SoccerField

def detail(request, pk):
    field = get_object_or_404(SoccerField, pk=pk)
    return render(request, 'soccer/field_detail.html', {'field': field})
