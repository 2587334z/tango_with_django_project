from django.db import models

# Create your models here.
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


class Category(models.Model):
    # Define attributes
    name_max_length = 128
    name = models.CharField(max_length=name_max_length, unique=True) # the value must be unique
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True) # Guarantee a unique match to an associated category

    # override save()
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)


    class Meta:
        verbose_name_plural = 'Categories'
        
    def __str__(self):
        return self.name

class Page(models.Model):
    # set max length
    title_max_length = 128
    url_max_length = 200
    # Define attributes
    category = models.ForeignKey(Category, on_delete=models.CASCADE) # one-to-many relationship
    title = models.CharField(max_length=title_max_length)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    # links UserProfile to user model instance
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # additional attributes
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username
