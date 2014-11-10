from django.db import models
from django.forms import ModelForm
from django import forms
from django.db.models import Avg
from django.db.models.signals import post_save
from django.db.models.signals import post_delete
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

class VoiceActor(models.Model):

  firstName = models.CharField (max_length = 50)
  fastName = models.CharField (max_length = 50)
  DOB = models.DateField(blank = True)
  
  def __unicode__(self):
        return self.firstName

class Director(models.Model):
  firstName = models.CharField(max_length = 50)
  lastName = models.CharField(max_length = 50)
  DOB = models.DateField(blank= True)
  def __unicode__(self):
        return self.firstName
  
  def get_absolute_url(self):
    return "/directors/%i/" % self.id


class Studio(models.Model):
  name = models.CharField(max_length = 100)
  city = models.CharField(max_length = 50, blank= True)
  def __unicode__(self):
        return self.name

class Anime(models.Model):
  title = models.CharField(max_length = 200)
  originalTitle = models.CharField(max_length = 200)
  genre = models.CharField(max_length = 50)
  year = models.IntegerField() 
  seriesNumber = models.IntegerField()
  directorFK = models.ForeignKey(Director)
  studioFK = models.ForeignKey(Studio)
  voiceActorFK = models.ManyToManyField(VoiceActor)
  rating = models.FloatField()
  description = models.CharField(max_length = 2000)

  def __unicode__(self):
    return self.title

  def get_absolute_url(self):
    return "/anime/%i/" % self.id
   


        

#class ActorAnime(models.Model):
  #voiceActorFK = models.ForeignKey (VoiceActor)
  #animeFK = models.ForeignKey (Anime)
 
    
class Rating (models.Model):
  userFK = models.ForeignKey(User)
  mark = models.FloatField()
  animeFK = models.ForeignKey(Anime, related_name='ratings')
  def __unicode__(self):
        return self.animeFK.title
 

class UserInfo (models.Model):
  user = models.OneToOneField(User)
  age = models.IntegerField (blank = True)
  country = models.CharField (blank= True, max_length = 40)
  def __unicode__(self):
        return self.user.username
  #def get_absolute_url(self):
   #return "/users/%s/" % self.username
  def get_absolute_url(self):
    return reverse('user.detail', kwargs={pk: self.id})
    

class Comments (models.Model):
  animeFK = models.ForeignKey(Anime)
  userFK = models.ForeignKey(User)
  text = models.CharField(max_length = 1000)
  def __unicode__(self):
        return self.animeFK.title

def get_rating (**kwargs):
  line = kwargs['instance'] 
  avgRating = line.animeFK.ratings.aggregate(Avg('mark'))
  print (avgRating)
  line.animeFK.rating = avgRating['mark__avg']
  line.animeFK.save()
  #Anime.objects.filter(originalTitle = line.)

post_save.connect (get_rating, sender = Rating)

post_delete.connect (get_rating, sender = Rating)
   
