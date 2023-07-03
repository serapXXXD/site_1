from django.contrib import admin
from authentication.models import Profile
from .models import Post, Category, Tag, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'body')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)


class TagAdmin(admin.ModelAdmin):
    list_display = ('title',)


class CommentAdmin(admin.ModelAdmin):
    ...


class ProfileAdmin(admin.ModelAdmin):
    ...


admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Profile, ProfileAdmin)
