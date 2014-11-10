from django import forms
from django.forms import ModelForm
from anime_content.models import Comments
from anime_content.models import Rating
from anime_content.models import UserInfo
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

class CommentsForm (ModelForm):
    text = forms.CharField(help_text = "Your comment: ", widget=forms.Textarea())
	
    class Meta:
        model = Comments
        fields = ['text']
   		
    #

class RatingForm (ModelForm):
    mark = forms.FloatField(help_text="Your mark: ")
	
    class Meta:
		model = Rating
		fields = ['mark']
    
    


class UserForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), help_text="Password")
    username = forms.CharField(help_text="Username")
    first_name = forms.CharField(help_text="Firstname")
    last_name = forms.CharField(help_text="Lastname")
    email = forms.CharField(help_text="Email")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password', 'email']

class UserInfoForm(ModelForm):
    age = forms.IntegerField(help_text="Age")
    country = forms.CharField(help_text="Country")

    class Meta:
        model = UserInfo
        fields = ['age', 'country']