from django.shortcuts import render
from soccer.models import SoccerField
from django.core.paginator import Paginator

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
