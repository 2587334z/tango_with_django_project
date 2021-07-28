from django.db import models

# Create your models here.
from django.template.defaultfilters import slugify


class Category(models.Model):
    # Define attributes
    name = models.CharField(max_length=128, unique=True) # the value must be unique
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
    # Define attributes
    category = models.ForeignKey(Category, on_delete=models.CASCADE) # one-to-many relationship
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title
