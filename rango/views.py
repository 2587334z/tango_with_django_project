from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.urls import reverse

from .forms import CategoryForm, PageForm, UserForm, UserProfileForm
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

    # handle the cookies
    visitor_cookie_handler(request)

    response = render(request, 'rango/index.html', context=context_dict)
    
    # return a rendered responsed to the client
    return response

def about(request):
    context_text = {}
    visitor_cookie_handler(request)
    context_text['visits'] = request.session['visits']
    return render(request, 'rango/about.html', context_text)

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

@login_required
def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            # save the value to database
            cat = form.save(commit=True)
            # confirm the category is being added
            print(cat, cat.slug)
            # redirect to ./rango
            return redirect('/rango')
        else:
            print(form.errors)

    return render(request, 'rango/add_category.html', {'form': form})

@login_required
def add_page(request, category_name_slug):
    # check the category is exist
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    if category is None:
        return redirect('/rango/')

    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                # save the value into database
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return redirect(reverse('rango:show_category', kwargs={'category_name_slug':category_name_slug}))
        else:
            print(form.errors)

    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context_dict)

def register(request):
    registered = False  # boolean - whether the registration was successful

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password) # hash the password
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            # if user submit the picture, get it
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)

    else:
        # if not a HTTP POST, blank these forms
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,
                  'rango/register.html',
                  {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password) # return a User object
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('rango:index'))
            else:
                # inactive account
                return HttpResponse("Your Rango account is disabled.")
        else:
            # invalid account
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied")
    else:
        # a HTTP GET
        return render(request, 'rango/login.html')

def some_view(request):
    if not request.user.is_authenticated():
        return HttpResponse("You are logged in.")
    else:
        return HttpResponse("You are not logged in.")

@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('rango:index'))

def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

def visitor_cookie_handler(request):
    # get the number of visits to the site
    visits = int(get_server_side_cookie(request, 'visits', '1'))

    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

    # if more than a day
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        # update the last visit cookie
        request.session['last_visit'] = str(datetime.now())
    else:
        # set the last visit cookie
        request.session['last_visit'] = last_visit_cookie

    # update/set the visits cookie
    request.session['visits'] = visits


