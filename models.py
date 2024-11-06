from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User

class Item(models.Model):
title = models.CharField(max_length=200) price = models.IntegerField()
discount_price = models.IntegerField(blank=True, null=True) slug = models.SlugField()
description = models.TextField()
image = models.ImageField(default='default.jpg',upload_to='static/img')

def  str (self): return self.title

def get_add_to_cart_url(self):
return reverse('add_to_cart', kwargs={'slug':self.slug})

def get_remove_from_cart_url(self):
return reverse('remove_from_cart', kwargs={'slug':self.slug})


def get_remove_single_from_cart_url(self):
return reverse('remove_single_from_cart', kwargs={'slug':self.slug})


class OrderItem(models.Model):
user = models.ForeignKey(User, on_delete=models.CASCADE) ordered = models.BooleanField(default=False)
item = models.ForeignKey(Item, on_delete=models.CASCADE) quantity = models.IntegerField(default=1)

def  str (self):
return f"{self.quantity} of {self.item.title}"

def get_total_item_price(self):
return (self.quantity * self.item.price)

def get_final_price(self):
return self.get_total_item_price()


class Order(models.Model):
user = models.ForeignKey(User, on_delete=models.CASCADE) items = models.ManyToManyField(OrderItem)
address = models.ForeignKey("Address", on_delete=models.SET_NULL, blank=Tr ue, null=True)
ordered = models.BooleanField(default=False) start_date = models.DateTimeField(auto_now_add=True) ordered_date = models.DateTimeField()

def  str (self):
return self.user.username


def get_total(self): total = 0
for order_item in self.items.all(): total += order_item.get_final_price()
return total


class Address(models.Model):
user = models.ForeignKey(User, on_delete=models.CASCADE) street_address = models.CharField(max_length=200) apartment_address = models.CharField(max_length=200) city = models.CharField(max_length=200)
pin = models.CharField(max_length=200) save_info = models.BooleanField(default=False) default = models.BooleanField(default=False)
use_default = models.BooleanField(default=False)
payment_option = models.CharField(choices=PAYMENT_CHOICES, max_length=2)

class Meta:
verbose_name_plural = 'Addresses'

def  str (self):
return self.user.username
