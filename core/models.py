from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.urls import reverse
from tinymce.models import HTMLField


# Create your models here.

class Construction(models.Model):
    class Meta:
        verbose_name = 'Typ konstrukcji'
        verbose_name_plural = 'Typ konstrukcji'
    name = models.CharField(max_length=20)
    slug = models.SlugField(max_length=20)

    def __str__(self):
        return self.name


class Additional(models.Model):
    class Meta:
        verbose_name = 'Dodatkowa zabudowa'
        verbose_name_plural = 'Dodatkowa zabudowa'
    name = models.CharField(max_length=20)
    slug = models.SlugField(max_length=20)

    def __str__(self):
        return self.name


class Cottage(models.Model):
    class Meta:
        verbose_name = 'Domki'
        verbose_name_plural = 'Domki'
    name = models.CharField(max_length=100, verbose_name="Unikalny identyfikator")
    slug = models.SlugField(unique=True, max_length=100)

    length = models.IntegerField(verbose_name="Długość")
    width = models.IntegerField(verbose_name="Szerokość")
    height = models.IntegerField(verbose_name="Wysokość")

    terrace_area = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, verbose_name="Powierzchnia tarasu")
    floor_area = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Powierzchnia podłogi")
    roof_area = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Powierzchnia dachu")

    number_of_rooms = models.IntegerField(default=1, verbose_name="Liczba pomieszczeń")

    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Cena")
    construction = models.ForeignKey(Construction, on_delete=models.CASCADE, verbose_name="Typ konstrukcji")
    additionals = models.ManyToManyField(Additional, blank=True, verbose_name="Dodatkowa zabudowa")

    transport_price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Cena transportu")

    description = HTMLField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('cottage', args=[self.slug])


class OptionalService(models.Model):
    class Meta:
        verbose_name = 'Dodatkowe usługi'
        verbose_name_plural = 'Dodatkowe usługi'
    class Choices(models.TextChoices):
        MONTAZ = 'MO', 'Montaż'
        MALOWANIE = 'MA', 'Malowanie'
        OKIENNICE = 'OK', 'Okiennice'
        RYNNY = 'RY', 'Rynny'
        KRYCIE_DACHU_PAPA = 'KP', 'Krycie dachu papą'
        KRYCIE_DACHU_GONTEM = 'KG', 'Krycie dachu gontem'
        KRYCIE_DACHU_BLACHODACHOWKA = 'KB', 'Krycie dachu blachodachówką'
        OCIEPLENIE_PODLOGI = 'OP', 'Ocieplenie podłogi'
        OCIEPLENIE_SCIAN = 'OS', 'Ocieplenie ścian'
        OCIEPLENIE_DACHU = 'OD', 'Ocieplenie dachu'
        TYNKOWANIE = 'TK', 'Tynkowanie'

    name = models.CharField(choices=Choices.choices, max_length=40, verbose_name="Nazwa")
    cottage = models.ForeignKey(Cottage, on_delete=models.CASCADE, verbose_name="Domek")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Cena")


def cottage_directory_path(instance, filename):
    return 'images/cottage_{0}/{1}'.format(instance.cottage.id, filename)


def gallery_directory_path(instance, filename):
    return 'images/gallery/{0}'.format(filename)


class CottagePhoto(models.Model):
    def __str__(self):
        return self.image.name
    class Meta:
        verbose_name = 'Zdjecia domków'
        verbose_name_plural = 'Zdjecia domków'
    image = models.ImageField(upload_to=cottage_directory_path, verbose_name="Zdjęcie")
    cottage = models.ForeignKey(Cottage, on_delete=models.CASCADE, related_name="cottage_photos", verbose_name="Domek")
    added_at = models.DateTimeField(auto_now_add=True)


class GalleryPhoto(models.Model):
    def __str__(self):
        return self.image.name
    class Meta:
        verbose_name = 'Galeria zdjęć (REALIZACJE)'
        verbose_name_plural = 'Galeria zdjęć (REALIZACJE)'
    image = models.ImageField(upload_to=gallery_directory_path, verbose_name="Zdjęcie")
    place = models.PositiveIntegerField(verbose_name="Pozycja")
    added_at = models.DateTimeField(auto_now_add=True)


@receiver(post_delete, sender=CottagePhoto)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)



