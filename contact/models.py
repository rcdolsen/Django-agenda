from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

# id (primary key - criado automáticamente pelo Django)
# first_name (string), last_name (string), phone (string)
# email (email), created_date (date), description (text)
# category (foreign key), show (boolean), picture (imagem)

# Depois
# owner (foreign key)


class Category(models.Model):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name


class Contact(models.Model):
    # blank=True serve para o campo nao ser obrigatorio
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=80, blank=True)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=254, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    description = models.TextField(blank=True)
    show = models.BooleanField(default=True)
    picture = models.ImageField(blank=True, upload_to='pictures/%Y/%m/%d')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, blank=True, null=True)
    owner = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
