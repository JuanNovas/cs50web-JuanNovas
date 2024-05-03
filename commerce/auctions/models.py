from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    pass



class Auction(models.Model):
    
    categorys = (
    ('ELEC', 'Electronics'),
    ('COMP', 'Computers'),
    ('SMH', 'Smart Home'),
    ('ARTS', 'Arts & Crafts'),
    ('AUTO', 'Automotive'),
    ('BABY', 'Baby'),
    ('BEAUTY', 'Beauty and Personal Care'),
    ('WOMEN', "Women's Fashion"),
    ('MEN', "Men's Fashion"),
    ('GIRLS', "Girl's Fashion"),
    ('BOYS', "Boy's Fashion"),
    ('HEALTH', 'Health and Household'),
    ('HOME', 'Home and Kitchen'),
    ('INDUSTRIAL', 'Industrial and Scientific'),
    ('LUGGAGE', 'Luggage'),
    ('MOVIES', 'Movies & Television'),
    ('PETS', 'Pet Supplies'),
    ('SOFTWARE', 'Software'),
    ('SPORTS', 'Sports and Outdoors'),
    ('TOOLS', 'Tools & Home Improvement'),
    ('TOYS', 'Toys and Games'),
    ('VIDEOGAMES', 'Video Games')
    )
    
    id = models.AutoField(primary_key=True)
    seller = models.ForeignKey(User, related_name='seller_auctions', on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=400,default="")
    start_bid = models.IntegerField()
    image = models.CharField(max_length=200, null=True)
    category = models.CharField(max_length=10, choices=categorys)
    active = models.BooleanField(default=True)
    bidder = models.ForeignKey(User, related_name='bidder_auctions', on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.name
    
class Bids(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Auction, on_delete=models.CASCADE)
    
class Comments(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Auction, on_delete=models.CASCADE)
    comment = models.CharField(max_length=240)
    
class Watchlist(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Auction, on_delete=models.CASCADE)