from django.db import models
# abstruct user import kortesi jeno user import korte pari
from django.contrib.auth.models import AbstractUser
from django.conf import settings



class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # ✅ Custom user model pointing
        on_delete=models.CASCADE,
        limit_choices_to={'user_type': 'seller'}  # শুধু seller রা add করতে পারবে
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Order(models.Model):
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Pending')
    

    def __str__(self):
        return f"{self.buyer.username} ordered {self.product.name}"

        # user alada kortesi buyer seller
class User(AbstractUser):
    user_type_choices = (
        ('buyer', 'buyer'),
        ('seller', 'seller'),
    )
    # user buyer na seller nije nije thik korte parbe
    user_type = models.CharField(
            max_length=10, # 10 digite string dite parbe
            choices= user_type_choices, # user choise dite parbe buyer naki seller
    )



