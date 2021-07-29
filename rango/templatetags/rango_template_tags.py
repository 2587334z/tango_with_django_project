from django import template
from rango.models import Category

# render the list of categories provide in the dictionary that is returned in the function
register = template.Library()

@register.inclusion_tag('rango/categories.html')
def get_category_list(current_category=None):
    # categories - a list of all the Category object present in the database
    return {'categories': Category.objects.all(),
            'current_category': current_category}