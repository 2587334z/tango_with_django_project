from django.contrib import admin
from rango.models import Category, Page

# Create a new class to custom the Page
class pageAdmin(admin.ModelAdmin):
    # Change the display
    list_display = ('title', 'category', 'url')

# Register the models here.
admin.site.register(Category)
admin.site.register(Page, pageAdmin)


