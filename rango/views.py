from django.shortcuts import render
from django.http import HttpResponse
from .models import Category, Page # Import the Category model

# Create your views here.
def index(request):
    # Retrieve the top five categories
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]

    # Build a dictionary to pass to the template engine as its context.
    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    context_dict['pages'] = page_list
    
    # return a rendered responsed to the client
    return render(request, 'rango/index.html', context_dict)

def about(request):
    return render(request, 'rango/about.html')

def show_category(request, category_name_slug):
    # Create a context dictionary which we can pass to the template rendering engine
    context_dict={}
    try:
        # Find a category name slug, if not, raises a DoesNotExist exception
        category = Category.objects.get(slug=category_name_slug)

        # Retrieve all of corresponding pages
        pages = Page.objects.filter(category=category)
        # Add corresponding pages from database to dictionary
        context_dict['pages'] = pages

        # Add the category object from database to dictionary
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None

    # render
    return render(request, 'rango/category.html', context_dict)


