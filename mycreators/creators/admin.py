from django.contrib import admin
from .models import Creator, Post

# Register your models here.

@admin.register(Creator)
class CreatorAdmin(admin.ModelAdmin):
    list_display = ('user', 'about_me', 'creator_type', 'status')
    list_filter = ('status', 'creator_type')
    actions = ['approve_creators', 'reject_creators']
    search_fields = ('user__username', 'about_me')

    def approve_creators(self, request, queryset):
        queryset.update(status='APPROVED')
    approve_creators.short_description = "Approve selected creators"

    def reject_creators(self, request, queryset):
        queryset.update(status='REJECTED')
    reject_creators.short_description = "Reject selected creators"
    
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('creator', 'content', 'created_at', 'updated_at')
    list_filter = ('creator', 'created_at')
    search_fields = ('creator__user__username', 'content')
    readonly_fields = ('created_at', 'updated_at')