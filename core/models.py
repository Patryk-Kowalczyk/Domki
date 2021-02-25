from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.urls import reverse
from tinymce.models import HTMLField

# Create your models here.

class Construction(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(max_length=20)
    def __str__(self):
        return self.name

class Additional(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(max_length=20)
    def __str__(self):
        return self.name

class Cottage(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=100)

    length = models.IntegerField()
    width = models.IntegerField()
    height = models.IntegerField()

    terrace_area = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    floor_area = models.DecimalField(max_digits=6, decimal_places=2)
    roof_area = models.DecimalField(max_digits=6, decimal_places=2)

    number_of_rooms = models.IntegerField(default=1)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    construction = models.ForeignKey(Construction, on_delete=models.CASCADE)
    additionals = models.ManyToManyField(Additional, blank=True, null=True)

    transport_price = models.DecimalField(max_digits=6, decimal_places=2)


    description = HTMLField()


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('cottage', args=[self.slug])

class OptionalService(models.Model):
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
    name = models.CharField(choices=Choices.choices, max_length=40)
    cottage = models.ForeignKey(Cottage, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)

def cottage_directory_path(instance, filename):
    return 'images/cottage_{0}/{1}'.format(instance.cottage.id, filename)

class CottagePhoto(models.Model):
    image = models.ImageField(upload_to=cottage_directory_path)
    cottage = models.ForeignKey(Cottage, on_delete=models.CASCADE, related_name="cottage_photos")
    added_at = models.DateTimeField(auto_now_add=True)

@receiver(post_delete, sender=CottagePhoto)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)






