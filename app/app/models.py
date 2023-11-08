from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.conf import settings
from django.utils.timezone import now 
from django.contrib.auth import get_user_model


class UserManager(BaseUserManager):
    def create_user(self, email, password):
        if not email:
            raise ValueError('Email not found')
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **args):
        if not email:
            raise ValueError('email is required')
        User = get_user_model()
        user = User.objects.create_user(email=self.normalize_email(email),password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(unique=False, default='')
    email = models.EmailField(unique=True)
    cpf = models.CharField(max_length=11, default='')  
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_vip = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        db_table = "user"

class Cart(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    itemsNumber = models.IntegerField()

    class Meta:
        db_table = "cart"

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=300)
    image_url = models.ImageField()
    #status = [sem estoque, baixo estoque, estoque normal]
    status = models.CharField(max_length=200, default="Sem Estoque")
    class Meta:
        db_table = "product"

class Order(models.Model):
    date = models.DateField(auto_now=True)
    status = models.CharField(max_length=100)
    totalValue = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey('User', on_delete=models.CASCADE, default=None)
    # address = models.ForeignKey('Address) 
    class Meta:
        db_table = "order"

class Item(models.Model):
    cart = models.ForeignKey('Cart', null=True, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, null=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    class Meta:
        db_table = "item"

class Stock(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    staff = models.ForeignKey('User', on_delete=models.CASCADE)
    modification_date = models.DateField(auto_now=True)
    quantity = models.IntegerField(default=0)

    class Meta:
        db_table = "stock"

class Address(models.Model):
    postal_code = models.CharField(max_length=11, default='')
    complement = models.CharField(max_length=200, default='')
    number = models.IntegerField(default=0)
    order = models.ForeignKey('Order',on_delete=models.CASCADE)

    class Meta:
        db_table = "address"