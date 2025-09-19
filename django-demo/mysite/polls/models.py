from django.db import models
from django.core.validators import RegexValidator,MinValueValidator


class Amenity(models.Model):
    name = models.CharField(max_length=100)  # Metin alanı
    description = models.TextField()         # Uzun metin alanı
    is_active = models.BooleanField(default=True)  # True/False alanı
    created_at = models.DateTimeField(auto_now_add=True)  # Otomatik tarih
    
    def __str__(self):
        return self.name

class Manager(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    hire_date = models.DateField()
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


class Property(models.Model):
    title = models.CharField(max_length=200)
    address = models.TextField()
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(0, message="Rent (price) cannot be negative.")
        ]
    )
    bedrooms = models.IntegerField(default=0)
    bathrooms = models.IntegerField(default=0)
   
    manager = models.ForeignKey('Manager', on_delete=models.CASCADE)
    amenities = models.ManyToManyField('Amenity')
    availability = models.BooleanField(default=False)
    zip_code = models.CharField(
        max_length=10,
        default='00000-0000',
        validators=[
            RegexValidator(
                regex=r'^\d{5}-\d{4}$',
                message='Zip code must be in the format 12345-6789'
            )
        ]
    )

    def __str__(self):
        return self.title

    def clean(self):
        super().clean()

        if (self.price is None or self.price == 0) and self.availability:
            raise ValidationError(
                "Property cannot be available if rent (price) is empty or zero."
            )