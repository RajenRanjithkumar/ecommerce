from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE ,null=True, blank=True)
    name = models.CharField(max_length=100, null=True )
    email = models.CharField(max_length=200, null=True)
   
    def __str__(self):
        return self.name
    
class Seller(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE ,null=True, blank=True)
    name = models.CharField(max_length=100, null=True )
    email = models.CharField(max_length=200, null=True)
   
    def __str__(self):
        return self.name


    

class Product(models.Model):

    CHOICES = (
        ('Phones', 'Phones'),
        ('Laptop', 'Laptops'),
        ('Tablets', 'Tablets'),
        ('Digital', 'Digital'),
    )

    name = models.CharField(max_length=100, null=True )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    digital = models.BooleanField(default=False, null=True, blank=False)
    #this requires the pillow lib
    image = models.ImageField(null=True, blank=True)
    seller = models.ForeignKey(Seller, null=True, on_delete=models.CASCADE)
    #customers = models.ManyToManyField(Customer, blank=True)
    category = models.CharField(choices=CHOICES, null=True, max_length=20)



    def __str__(self):
        return self.name
    
    # if the image doesnt exist
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ""
        return url

    
class Order(models.Model):

    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    data_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    trasacrion_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)
    
    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()

        for item in orderitems:
            if item.product.digital == False:
                #its a physical product
                shipping = True
        return shipping
    

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
    #gets all the cart items from the DB
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    
class OrderItem(models.Model):

    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    data_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):

        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=100, null=True )
    city = models.CharField(max_length=100, null=True )
    state = models.CharField(max_length=100, null=True )
    zipcode = models.CharField(max_length=100, null=True )
    data_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.address)


