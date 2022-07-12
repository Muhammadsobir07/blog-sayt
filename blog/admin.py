from django.contrib import admin
from .models import Post,Comment


# admin.site.register(Post)
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_displey = ['title','author','publish','status']
    list_display = ('status','created', 'publish' , 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publish'
    ordering = ('status','publish',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name','email','post','created','activate')
    list_filter = ('activate','created','update')
    search_fields = ('name','email','body')
















