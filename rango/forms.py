from django import forms
from .models import Page, Category, User, UserProfile

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=Category.name_max_length, help_text="Please enter the category name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(),required=False)

    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Category
        fields = ('name',)

class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=Page.title_max_length, help_text="Please enter the title of the page.")
    url = forms.URLField(max_length=Page.url_max_length, help_text="Please enter the URL of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput, initial=0)

    class Meta:
        # Provide an association between the ModelForm and a model
        model = Page
        exclude = ('category',)

    def clean(self):
        cleaned_data = self.cleaned_data

        # check if the value of url field entered by the user starts with http:// – and
        # if it doesn’t, we can prepend http:// to the user’s input.
        url = cleaned_data.get('url') # obtain the form's values
        if url and not url.startswith('http://'):
            url = f'http://{url}'
            cleaned_data['url'] = url
        return cleaned_data

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    # additional properties about the particular class to which it belongs
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    # additional properties about the particular class to which it belongs
    class Meta:
        model = UserProfile
        fields = ('website', 'picture',)

