from django.conf.urls import patterns, url
from anime_content.views import AnimeList
from anime_content.views import AnimeDetail
from anime_content.views import UserList
from anime_content.views import UserDetail
from anime_content.views import DirectorDetail
from anime_content.views import VoiceActorDetail
from anime_content.views import DirectorList
from anime_content.views import VoiceActorList
from anime_content.views import UserSearch
from anime_content.views import AnimeSearch
from anime_content.views import DirectorSearch
from anime_content.views import VoiceActorSearch
from anime_content.views import CommentsFormView
from anime_content.views import AnimeByVoiceActor
from anime_content.views import AnimeByDirector
from anime_content.views import AnimeByStudio
from anime_content.views import register
from anime_content.views import index
from anime_content.views import user_login
from anime_content.views import restricted
from anime_content.views import user_logout
from anime_content.views import RatingCreateView
from anime_content.views import CommentsCreateView
from django.contrib.auth.decorators import login_required
#from anime_content.views import add_rating


urlpatterns = patterns('',
    #url(r'^$', views.index, name='index'),
    url(r'^index/$', index, name='index'),
    url(r'^anime/$', AnimeList.as_view(), name='anime_list'),

    url(r'^anime/(?P<pk>\d+)/$', AnimeDetail.as_view(),  name='anime.detail'),
    url(r'^anime/(?P<pk>\d+)/addcomment/$', login_required(CommentsCreateView.as_view()), name='anime.comment'),
    url(r'^anime/(?P<pk>\d+)/addrating/$', login_required(RatingCreateView.as_view()),  name='anime.rating'),
    url(r'^users/$', UserList.as_view(), name = 'user.list'),
    url(r'^users/(?P<pk>\d+)/$', UserDetail.as_view(template_name = 'anime/user_details.html', 
        context_object_name = 'user_detail'), name = 'user.detail'),
    url(r'^anime/search/$', AnimeSearch.as_view()),
    url(r'^users/search/$', UserSearch.as_view() ),
    url(r'^directors/$', DirectorList.as_view(), name='director.list'),
    url(r'^voice/$', VoiceActorList.as_view()),
    url(r'^directors/(?P<pk>\d+)/$', DirectorDetail.as_view(), name = 'director.detail'),
    url(r'^voice/(?P<pk>\d+)/$', VoiceActorDetail.as_view()),
    url(r'^directors/search/$', DirectorSearch.as_view()),
    url(r'^voice/search/$', VoiceActorSearch.as_view()),
    url(r'^voice/(?P<pk>\d+)/anime/$', AnimeByVoiceActor.as_view()),
    url(r'^directors/(?P<pk>\d+)/anime/$', AnimeByDirector.as_view()),
    url(r'^studio/(?P<pk>\d+)/anime/$', AnimeByStudio.as_view()),
    url(r'^anime/(?P<cid>\d+)/addcomment/$', CommentsFormView.as_view()),
    url(r'^register/$', register, name='register'),
    #url(r'^register/$', register, name='register'),
    url(r'^login/$', user_login, name='login'),
    url(r'^restricted/', restricted, name='restricted'),
    url(r'^logout/$', user_logout, name='logout'),
)
