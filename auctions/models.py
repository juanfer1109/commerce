from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Category(models.Model):
    catName = models.CharField(max_length=40)

    def __str__(self):
        return self.catName

class Listing(models.Model):
    title = models.CharField(max_length=40)
    description = models.TextField()
    image_url = models.CharField(max_length=500)
    is_active = models.BooleanField(default=True)
    starting_bid = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='user')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, related_name='category')
    watch = models.ManyToManyField(User, blank=True, null=True, related_name="watch")

    def __str__(self):
        return self.title

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='user_comment')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True, blank=True, related_name='listing_comment')
    comment = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.author} - {self.listing}"

class Bid (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='user_bid')
    bid = models.FloatField(default=0)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='listing_bid')


