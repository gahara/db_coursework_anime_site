# Create your views here.
from django.http import HttpResponse
from django.views.generic import ListView
from django.views.generic import DetailView
from anime_content.models import Anime, UserInfo, VoiceActor, Director, Studio, Comments
from django.contrib.auth.models import User
from anime_content.forms import CommentsForm, UserForm, UserInfoForm, RatingForm
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django import forms 
from django.views.generic.edit import FormMixin
from anime_content.forms import RatingForm
from django.views.generic import FormView
from django.views.generic.detail import SingleObjectMixin
from django.core.exceptions import PermissionDenied
import pdb



#def index(request):
    #return HttpResponse("You're at the anime index.")
def index(request):
    print "hohh"
    context = RequestContext(request)
    return render_to_response('anime/index.html', context)

def profile_view(request, username):
    u = User.objects.get(username=username)
    return u
class RatingCreateView(CreateView):
  form_class = RatingForm
  
  
  def post(self, request, *args, **kwargs):
    self.pk = kwargs['pk']
    self.user= request.user
    return super(RatingCreateView, self).post(request, *args, **kwargs)

  def get(self, request, *args, **kwargs):
    raise PermissionDenied

  
  def form_valid(self, form):
    rating = form.save(commit=False)
    rating.userFK = self.user
    rating.animeFK = Anime.objects.get(pk=self.pk)
    rating.save()
    return super(RatingCreateView, self).form_valid(form)

  def get_success_url(self):
        return reverse('anime.detail', kwargs={'pk': self.pk})

class CommentsCreateView(CreateView):
  form_class = CommentsForm
  
  def post(self, request, *args, **kwargs):
    self.pk = kwargs['pk']
    self.user= request.user
    return super(CommentsCreateView, self).post(request, *args, **kwargs)

  def get(self, request, *args, **kwargs):
    raise PermissionDenied

  
  def form_valid(self, form):
    comment = form.save(commit=False)
    comment.userFK = self.user
    comment.animeFK = Anime.objects.get(pk=self.pk)
    comment.save()
    return super(CommentsCreateView, self).form_valid(form)

  def get_success_url(self):
        return reverse('anime.detail', kwargs={'pk': self.pk})

   
class AnimeByVoiceActor (ListView):
  queryset = Anime.voiceActorFK

class AnimeByDirector (ListView):
  queryset = Anime.directorFK

class AnimeByStudio (ListView):
  queryset = Anime.studioFK

class StudioList (ListView):
  queryset = Studio.objects.order_by('-name')

class StudioDetail(DetailView):
  model = Studio

class studioSearch(ListView):
  #template
  def get_queryset(self):
    return Studio.objects.filter(name__contains=self.request.GET['q'])

class VoiceActorList(ListView):
  queryset = VoiceActor.objects.order_by('-firstName')

class VoiceActorDetail(DetailView):
  model = VoiceActor

class VoiceActorSearch(ListView):
  #template
  def get_queryset(self):
    return VoiceActor.objects.filter(firstName__contains=self.request.GET['q'])

class DirectorList(ListView):
  queryset = Director.objects.order_by('-firstName')
  template_name = "anime/director_list.html"
  context_object_name = "director_list"

class DirectorDetail(DetailView):
  model = Director
  template_name = "anime/director_details.html"
  context_object_name = "director_detail"

class UserList(ListView):
  queryset = UserInfo.objects.order_by('-username')
  template_name = "anime/user_list.html"
  context_object_name = "user_list"

class UserDetail(DetailView):
  model = UserInfo


  


class DirectorSearch(ListView):
  #template
  def get_queryset(self):
    return Director.objects.filter(firstName__contains=self.request.GET['q'])

class AnimeList(ListView):
    #model = tblAnime
  queryset = Anime.objects.order_by('-originalTitle')
  template_name = "anime/anime_list.html"
  context_object_name = "anime_list"



class AnimeDetail(DetailView):
  template_name = 'anime/anime_details.html' 
  model = Anime
  context_object_name = "anime_detail"
  def get_context_data(self, **kwargs):
    context = super(AnimeDetail, self).get_context_data(**kwargs)
    context['rating_form'] = RatingForm()
    context['comment_form'] = CommentsForm()
    context['show_comments'] = Comments.objects.filter(animeFK = self.object)

    return context


class UserList(ListView):
	model = UserInfo


class UserDetail(DetailView):
	model = UserInfo

class AnimeSearch(ListView):
	#template
	def get_queryset(self):
		return Anime.objects.filter(originalTitle__contains=self.request.GET['q'])

class UserSearch(ListView):
	def get_queryset(self):
		return User.objects.filter(username__contains=self.request.GET['q'])

class CommentsFormView(CreateView):
#template_name
	form_class = CommentsForm
	
	def get_success_url(self):
   		return reverse('anime.detail', kwargs={pk: self.request.kwargs['cid']})

   	@method_decorator(login_required)
   	def __call__ (self, request, **kwargs):
      
   		super(CommentsFormView, self).__call__(request, **kwargs)

   	def get_form_kwargs(self):
   		args = super(CommentsFormView, self).get_form_kwargs()
   		comment = Comments(toAnime=self.request.kwargs['cid'], fromUser=self.user.id)
   		args['instance'] = comment
   		return comment






def register(request):
    
    context = RequestContext(request)
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user

            
            profile.save()

            
            registered = True

        else:
            print user_form.errors, profile_form.errors

 
    else:
        user_form = UserForm()
        profile_form = UserInfoForm()

    
    return render_to_response(
            'anime/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
            context)


def user_login(request):
    
    context = RequestContext(request)

   
    if request.method == 'POST':
        
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/index/')
            else:
                
                return HttpResponse("Your account is disabled.")
        else:
            
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

  
    else:
        
        return render_to_response('anime/login.html', {}, context)

def some_view(request):
    if not request.user.is_authenticated():
        return HttpResponse("You are logged in.")
    else:
        return HttpResponse("You are not logged in.")


@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")

@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/index/')



