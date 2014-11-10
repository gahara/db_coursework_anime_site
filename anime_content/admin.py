from django.contrib import admin
from anime_content.models import Anime
from anime_content.models import Director
from anime_content.models import Studio
from anime_content.models import VoiceActor
from anime_content.models import Rating
from anime_content.models import UserInfo
from anime_content.models import Comments

admin.site.register(Anime)
admin.site.register(Director)
admin.site.register(Studio)
admin.site.register(VoiceActor)
admin.site.register(Rating)
admin.site.register(UserInfo)
admin.site.register(Comments)
