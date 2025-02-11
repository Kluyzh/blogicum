from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .models import Category, Comment, Location, Post, User

admin.site.unregister(Group)
admin.site.unregister(User)


admin.site.empty_value_display = 'Не задано'


class CustomUserAdmin(UserAdmin):
    list_display = (
        'first_name',
        'last_name',
        'username'
    )


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'category',
        'location',
        'title',
        'text',
        'pub_date',
        'is_published'
    )
    list_editable = (
        'is_published',
    )
    search_fields = (
        'text',
    )
    list_filter = (
        'category',
        'author'
    )


class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'created_at'
    )


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'description',
        'is_published'
    )
    list_editable = (
        'is_published',
    )


admin.site.register(Comment)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(User, CustomUserAdmin)
