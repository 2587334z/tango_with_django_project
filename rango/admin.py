from django.contrib import admin
from .models import Category, Page


# Create a new class to custom the Page
class pageAdmin(admin.ModelAdmin):
    # Change the display
    list_display = ('title', 'category', 'url')

# Customise the Admin Interface
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

# Register the models here.
admin.site.register(Category,CategoryAdmin)
admin.site.register(Page, pageAdmin)


