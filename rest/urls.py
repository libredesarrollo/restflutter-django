
from django.urls import path

from . import views

app_name='api'
urlpatterns = [
    #********Botones
    path('button/all',views.ButtonList.as_view()),
    #path('button/group/<int:group_id>',views.ButtonGroup.as_view()),
    path('button/group/<int:group_id>',views.button_group),
    path('button',views.ButtonListPagination.as_view()),
    path('button/<int:pk>',views.ButtonDetail.as_view()),
    #********Chips
    path('chip/all',views.ChipList.as_view()),
    #path('button/group/<int:group_id>',views.ButtonGroup.as_view()),
    path('chip/group/<int:group_id>',views.chip_group),
    path('chip',views.ChipListPagination.as_view()),
    path('chip/<int:pk>',views.ChipDetail.as_view()),
    #********Imagenes
    path('image/all',views.ImageList.as_view()),
    #path('button/group/<int:group_id>',views.ButtonGroup.as_view()),
    path('image/group/<int:group_id>',views.image_group),
    path('image',views.ImageListPagination.as_view()),
    path('image/<int:pk>',views.ImageDetail.as_view()),
    #********Textos
    path('text/all',views.TextList.as_view()),
    #path('button/group/<int:group_id>',views.ButtonGroup.as_view()),
    path('text/group/<int:group_id>',views.text_group),
    path('text',views.TextListPagination.as_view()),
    path('text/<int:pk>',views.TextDetail.as_view()),
    #********Grupos
    path('group/all',views.GroupList.as_view()),
    path('group/<int:pk>',views.GroupDetail.as_view()),
    #********Mixs
    path('mix/<int:group_id>',views.mix_group),
    path('login',views.login),
    path('logout',views.logout),
    path('verify',views.verify),
    
    
]


#viewset

from rest_framework import routers
from .viewset import NoteViewSet

route = routers.SimpleRouter()
route.register('note',NoteViewSet)

urlpatterns += route.urls