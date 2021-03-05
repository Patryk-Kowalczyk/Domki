import math

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Cottage, CottagePhoto, Construction, Additional
from .forms import ContactForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.mail import send_mail
from django.contrib import messages

# Create your views here.

def send_contact_mail(data, cottage=None):
    message = 'Otrzymano wiadomość od: {} \n'.format(data.get('first_name'))
    if cottage:
        message += 'Dotyczącą domku: {}\n'.format(cottage.name)
    else:
        'Z prośbą o kontakt\n'
    if data.get('contact_mail'):
        message += 'Email: {}\n'.format(data.get('contact_mail'))
    if data.get('phone_number'):
        message += 'Numer kontaktowy: {}\n'.format(data.get('phone_number'))
    if cottage:
        message += 'Dodatkowe opcje wybrane przy domku: \n'
        for item, value in data.items():
            if value == 'on':
                service = cottage.optionalservice_set.get(name=item)
                message += ' - ' + service.get_name_display() + f' ({service.price}zł)' + '\n'
        message += f'O szacowanej całkowitej wartości: {data["form-price"]}zł'
    send_mail(
        "Nowa prośba o kontakt",
        message,
        'ixe.007@gmail.com',
        ['ixe.007@gmail.com'],
        fail_silently=False,
    )
    return True


def filter(request):
    qs = Cottage.objects.all()

    url_query_dict = dict(request.GET)

    if url_query_dict.get('constructions'):
        qs = qs.filter(construction__name__in=url_query_dict.get('constructions'))
    if url_query_dict.get('floor_area'):
        area = int(url_query_dict.get('floor_area')[0])
        qs = qs.filter(floor_area__lte=area)
    if url_query_dict.get('additionals'):
        qs = qs.filter(additionals__name__in=url_query_dict.get('additionals'))
    if url_query_dict.get('height'):
        height = int(url_query_dict.get('height')[0])
        qs = qs.filter(height__lte=height)
    if url_query_dict.get('terrace'):
        terrace = url_query_dict.get('terrace')[0]
        if terrace == "on":
            qs = qs.filter(terrace_area__isnull=False)
    if url_query_dict.get('rooms'):
        rooms = url_query_dict.get('rooms')[0]
        if rooms == "1":
            qs = qs.filter(number_of_rooms="1")
        elif rooms == "2-3":
            qs = qs.filter(number_of_rooms__in=["2", "3"])
        elif rooms == "Więcej":
            qs = qs.filter(number_of_rooms__gt=3)
    if url_query_dict.get('price-min'):
        qs = qs.filter(price__gte=math.floor(float(url_query_dict.get('price-min')[0])-1))
        qs = qs.filter(price__lte=math.ceil(float(url_query_dict.get('price-max')[0])+1))
    return qs, url_query_dict

def index(request):
    constructions = Construction.objects.all()
    additionals = Additional.objects.all()

    class ValuesOfArea:
        list = Cottage.objects.values_list('floor_area')
        if list:
            min = math.floor(list.order_by('floor_area').first()[0])
            max = math.ceil(list.order_by('floor_area').last()[0])

    class ValuesOfHeight:
        list = Cottage.objects.values_list('height')
        if list:
            min = math.floor(list.order_by('height').first()[0])
            max = math.ceil(list.order_by('height').last()[0])

    class ValuesOfPrice:
        list = Cottage.objects.values_list('price')
        if list:
            min = math.floor(list.order_by('price').first()[0])
            max = math.ceil(list.order_by('price').last()[0])


    qs, params = filter(request)
    paginator = Paginator(qs, "8")
    page_number = request.GET.get('page')

    try:
        qs = paginator.page(page_number)
    except PageNotAnInteger:
        qs = paginator.page(1)
    except EmptyPage:
        qs = paginator.page(paginator.num_pages)

    return render(request, "pages/homepage.html", {
        "constructions": constructions,
        "cottages": qs,
        "additionals": additionals,
        "floor_area": ValuesOfArea,
        "height": ValuesOfHeight,
        "price": ValuesOfPrice,
        "params": params,
    })

def about(request):
    return render(request, "pages/aboutpage.html")

def plots(request):
    return render(request, "pages/plots.html")

def contact(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            data = request.POST
            send_contact_mail(data, True)
            messages.success(request, "Pomyślnie wysłano prośbę o kontakt")
    return render(request, "pages/contact.html", {'form': form})

def cottage(request, slug):
    cottage = get_object_or_404(Cottage, slug=slug)
    images = CottagePhoto.objects.filter(cottage=cottage)
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            data = request.POST
            send_contact_mail(data, True)
            messages.success(request, "Pomyślnie wysłano prośbę o kontakt")

    return render(request, "pages/cottagepage.html", {
        'cottage': cottage,
        'images': images,
        'form': form,
    })
