from django.urls import path
from .views import post_detail,post_List,post_share

app_name = 'blog'

urlpatterns = [
    path('',post_List, name="post_list"),

    path('tag/<slug:tag_slug>/',post_List, name='post_list_by_tag'),

    path('<int:year>/<int:month>/<int:day>/<slug:post>/',post_detail,name="post_detail"),
    path('<int:post_id>/share/',post_share, name='post_share'),
]


