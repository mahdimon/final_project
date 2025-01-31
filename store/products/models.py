from django.db import models
from core.models import BaseModel
from safedelete.models import SOFT_DELETE,HARD_DELETE,SOFT_DELETE_CASCADE

class Discount(BaseModel):
    _safedelete_policy = HARD_DELETE
    PERCENTAGE = 'p'
    FIXED = 'f'
    
    DISCOUNT_TYPE_CHOICES = [
        (PERCENTAGE, 'Percentage'),
        (FIXED, 'Fixed'),
    ]

    discount_type = models.CharField(
        max_length=1,
        choices=DISCOUNT_TYPE_CHOICES,
        blank=False,
        null=False,
        verbose_name="Discount Type"
    )
    value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Discount Value"
    )
    max_discount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Maximum Discount"
    )

    class Meta:
        verbose_name = "Discount"
        verbose_name_plural = "Discounts" 
 

    def __str__(self):
        return f"{self.get_discount_type_display()} - {self.value}"
class Product(BaseModel):
    _safedelete_policy = SOFT_DELETE
    
    image = models.ImageField(upload_to='product_images/',null=True,blank=True)
    name = models.CharField(max_length=150, null=False)
    brand = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    stock = models.IntegerField(default=0, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    category = models.ForeignKey(
        'Category', 
        on_delete=models.SET_NULL, 
        blank=True, 
        null=True,
        related_name='products'
    )
    discount = models.ForeignKey(
        Discount, 
        on_delete=models.SET_NULL, 
        null=True,
        blank=True,
        related_name='products'
    )

    class Meta:
        verbose_name = "Product"  
        verbose_name_plural = "Products" 
        ordering = ['name'] 
    
    def calculate_discounted_price(self):
        discount :Discount= self.discount
        if discount:
            if discount.discount_type == Discount.PERCENTAGE:
                max_discount = discount.max_discount if discount.max_discount is not None else float('inf')
                return self.price - min((self.price * discount.value / 100), max_discount)
            elif discount.discount_type == Discount.FIXED:
                return self.price - discount.value
        return self.price
        
class Category(BaseModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    
    name = models.CharField(max_length=150, null=False)
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True,
        related_name='subcategories'
    )
    
    class Meta:
        verbose_name = "Category"  
        verbose_name_plural = "Category" 
        ordering = ['name'] 
    
    def __str__(self):
        return self.name


