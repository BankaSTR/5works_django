from django.db import models
from users.models import User
# Create your models here.
class Basket(models.Model):
	user = models.OneToOneField(User,null=True,on_delete=models.CASCADE)


class Product(models.Model):
	title = models.CharField(max_length=55)
	price = models.PositiveIntegerField(default=0)
	categories = models.ManyToManyField("Category")
	image = models.ImageField(upload_to='photos')
	country = models.CharField(max_length=50)  # Новое поле для страны производителя
	manufacture_year = models.IntegerField()  # Новое поле для года производства
	model = models.CharField(max_length=50)  # Новое поле для модели товара
	availability = models.PositiveIntegerField(default=0)

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class In_Basket(models.Model):
	basket = models.ForeignKey(Basket,related_name="basket_of_user",on_delete=models.CASCADE)
	prodcut = models.ForeignKey(Product,related_name='product_of_user',on_delete=models.CASCADE)
	quantity = models.PositiveIntegerField(default=1)

class Order(models.Model):
	user = models.ForeignKey(User, related_name="order_user", on_delete=models.CASCADE)
	data = models.DateField(auto_now=True)
	id = models.IntegerField(unique=True, primary_key=True)
	total_cost = models.PositiveIntegerField(default=0)
	STATUS_CHOICES = (
		('Новый', 'Новый'),
		('Отменён', 'Отменен'),
		('Подтверждён', 'Подтвержден'),
	)
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Новый')
	massage = models.CharField(max_length=500, default='Примечание', null=True)

class In_Order(models.Model):
	order = models.ForeignKey(Order, related_name="order_of_user", on_delete=models.CASCADE)
	prodcut = models.ForeignKey(Product, related_name='product_of_order', on_delete=models.CASCADE)
	quantity = models.PositiveIntegerField(default=1)