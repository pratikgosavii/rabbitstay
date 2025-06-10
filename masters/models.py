

from django.db import models


from users.models import User
from django.utils.timezone import now
from datetime import datetime, timezone

import pytz
ist = pytz.timezone('Asia/Kolkata')



from users.models import User





class amenity(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class room_amenity(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class room_type(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class coupon(models.Model):

    TYPE_CHOICES = [
        ('percent', 'Percentage'),
        ('amount', 'Amount'),
    ]
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='percent')  # 👈 Add this

    code = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500, null=True, blank=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    min_purchase = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    max_discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='doctor_images/')
    start_date = models.DateTimeField(default=now)
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.code


class service_category(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='product_images/')
    description = models.TextField()

    def __str__(self):
        return self.name


class service_subcategory(models.Model):
    category = models.ForeignKey(service_category, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


class service(models.Model):
    category = models.ForeignKey(service_category, on_delete=models.CASCADE, null=True, blank=True)
    subcategory = models.ForeignKey(service_subcategory, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField()  
    image = models.ImageField(upload_to='symptom_images/', null=True, blank=True)
    price = models.IntegerField()

    def __str__(self):
        return self.name


class symptom(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='symptom_images/', null=True, blank=True)

    def __str__(self):
        return self.name


class customer_address(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    address = models.TextField()
    landmark = models.CharField(max_length=255, null=True, blank=True)
    pin_code = models.CharField(max_length=10)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)

    def __str__(self):
        return (
            f"Name: {self.name}, "
            f"Type: {self.type}, "
            f"Address: {self.address}, "
            f"Landmark: {self.landmark or 'N/A'}, "
            f"Pin Code: {self.pin_code}, "
            f"City: {self.city}, "
            f"State: {self.state}"
        )



class testimonials(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class test(models.Model):
    name = models.CharField(max_length=120)
    image = models.ImageField(upload_to='doctor_images/')
    rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    description = models.CharField(max_length=120, null=True, blank=True)
    mrp = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class dog_breed(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name



class cat_breed(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class product_category(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='product_images/')


    def __str__(self):
        return self.name



class product(models.Model):
    
    name = models.CharField(max_length=255)
    category = models.ForeignKey(product_category, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='product_images/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0, null=True, blank=True)
    is_popular = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name





from django.db import models

class vaccination(models.Model):
    name = models.CharField(max_length=100)
    disease = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    age_limit = models.PositiveIntegerField(help_text="Recommended age in weeks/months/years")
    date_created = models.DateTimeField(auto_now_add=True)
    price = models.IntegerField()

    def __str__(self):
        return self.name
    

class event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='doctor_images/')
    start_date = models.DateTimeField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class food_menu(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='doctor_images/')
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name





class home_banner(models.Model):
    title = models.CharField(max_length=225, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='homeBanners/')
    is_for_web = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    






class consultation_type(models.Model):
    title = models.CharField(max_length=225, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.IntegerField()
    image = models.ImageField(upload_to='homeBanners/')
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    



class online_consultation_type(models.Model):
    title = models.CharField(max_length=225, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='homeBanners/')
    price = models.IntegerField()
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    




