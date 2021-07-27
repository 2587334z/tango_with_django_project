from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    # build a dictionary to pass to the template engine as its context.
    # the key boldmessage to match the {{ boldmessage}} variable in template/rango/index.html
    context_dict = {'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!'}
    
    # return a rendered responsed to the client
    return render(request, 'rango/index.html', context_dict)

def about(request):
    return render(request, 'rango/about.html')