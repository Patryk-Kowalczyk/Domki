import math

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Cottage, CottagePhoto, Construction, Additional
from .forms import ContactForm

# Create your views here.

def filter(request):
    qs = Cottage.objects.all()
    constructions = Construction.objects.all()

    url_query_dict = dict(request.GET)

    if url_query_dict.get('constructions'):
        qs = qs.filter(construction__name__in=url_query_dict.get('constructions'))
    if url_query_dict.get('floor_area'):
        area = int(url_query_dict.get('floor_area')[0])
        qs = qs.filter(floor_area__lte=area)


    return qs

def index(request):
    constructions = Construction.objects.all()
    additionals = Additional.objects.all()

    class ValuesOfArea:
        list = Cottage.objects.values_list('floor_area')
        min = math.floor(list.order_by('floor_area').first()[0])
        max = math.ceil(list.order_by('floor_area').last()[0])

    class ValuesOfHeight:
        list = Cottage.objects.values_list('height')
        min = math.floor(list.order_by('height').first()[0])
        max = math.ceil(list.order_by('height').last()[0])


    qs = filter(request)
    return render(request, "pages/homepage.html", {
        "constructions": constructions,
        "cottages": qs,
        "additionals": additionals,
        "floor_area": ValuesOfArea,
        "height": ValuesOfHeight,
    })

def about(request):
    return render(request, "pages/aboutpage.html")

def cottage(request, slug):
    cottage = get_object_or_404(Cottage, slug=slug)
    images = CottagePhoto.objects.filter(cottage=cottage)
    if request.method == 'POST':
        form = ContactForm(request.POST)
        print(request.POST)
        #if form.is_valid():
            #print(form.cleaned_data)
        return HttpResponse("Ok")
    else:
        form = ContactForm()
        return render(request, "pages/cottagepage.html", {
            'cottage': cottage,
            'images': images,
            'form': form,
        })
