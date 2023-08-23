from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    category_name = models.CharField(max_length=30)

    def __str__(self):
        return self.category_name




class Listing(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=300)
    image_url = models.CharField(max_length=3000, null=True, blank=True)
    current_bid = models.FloatField()
    is_active = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="users")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category")
    time = models.DateTimeField(auto_now_add=True, null=True)
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="watchlist")

    def __str__(self):
        return self.title
    
class Bid(models.Model):
    bid = models.FloatField()
    bid_user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="bid_user")
    bid_time = models.DateTimeField(auto_now_add=True)
    bid_listing = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True, blank=True, related_name="bid_listing")

    def __str__(self):
        return f"{self.bid_user} bidded {self.bid} at {self.bid_time}"

class Comment(models.Model):
    comment_author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="comment_author")
    comment_listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="comment_listing") 
    comment_content = models.CharField(max_length=500)   
    comment_time = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.comment_author} - {self.comment_time}"


    

