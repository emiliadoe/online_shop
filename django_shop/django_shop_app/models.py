from django.db import models
from django.contrib.auth.models import User
from django.conf import settings



class Product(models.Model):

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Product'

    TYPE = [
        ('S', 'Schokolade'),
        ('G', 'Gummibaerchen'),
        ('K', 'Kaugummis'), 
        ('B', 'Bonbons'),
        ('So', 'Sonstiges')
    ]

    category = models.CharField(
        max_length=2,
        choices=TYPE
    )

    title = models.CharField(max_length=50)

    price= models.DecimalField(max_digits=10, decimal_places=2)

    description = models.CharField(max_length=400)

    image = models.ImageField(upload_to='product_images', blank=True, null=True)

    pdf = models.FileField(upload_to='product_pdfs', blank=True, null=True)
    
    def __str__(self):
        return self.title


class Rating(models.Model):

    text = models.TextField(max_length=500)
    rating = models.IntegerField(choices=[(i, f'{i} Sterne') for i in range(1, 6)], default=3)  # 1-5 Sterne Bewertung
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        ordering = ['timestamp']
        verbose_name = 'Rating'
        verbose_name_plural = 'Ratings'
        unique_together = ('user', 'product')

    def get_comment_excerpt(self):
        if len(self.text) > 50:
            return self.text[:50] + '...'
        else:
            return self.text

    def __str__(self):
        return f'{self.get_comment_excerpt()} ({self.user.username})'

    def __repr__(self):
        return f'{self.get_comment_excerpt()} ({self.user.username} / {str(self.timestamp)})'
    

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"


class ReviewVote(models.Model):
    VOTE_CHOICES = [
        ('helpful', 'Helpful'),
        ('not_helpful', 'Not Helpful'),
    ]

    vote_type = models.CharField(max_length=11, choices=VOTE_CHOICES)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'rating')

class Report(models.Model):
    REASON_CHOICES = [
        ('spam', 'Spam'),
        ('offensive', 'Offensive'),
        ('other', 'Other')
    ]

    reason = models.CharField(max_length=10, choices=REASON_CHOICES)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('user', 'rating')

""" 
class Vote(models.Model):

    VOTE_TYPES = [
        ('1', '1'),
        ('2', '2'),
    ]

    up_or_down = models.CharField(max_length=1, choices=VOTE_TYPES)

    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    holiday_housing = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.up_or_down} on {self.holiday_housing} by {self.user.username}'

    def __repr__(self):
        return f'{self.up_or_down} on {self.holiday_housing} by {self.user.username} ({self.timestamp})'

 """