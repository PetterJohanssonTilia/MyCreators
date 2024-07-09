from django.contrib import admin
from .models import Creator, Post

# Register your models here.

@admin.register(Creator)
class CreatorAdmin(admin.ModelAdmin):
    list_display = ('user', 'about_me')
    search_fields = ('user__username', 'about_me')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('creator', 'content', 'created_at', 'updated_at')
    list_filter = ('creator', 'created_at')
    search_fields = ('creator__user__username', 'content')
    readonly_fields = ('created_at', 'updated_at')