from django.contrib import admin

from .models import *


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'body')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)

class TagAdmin(admin.ModelAdmin):
    list_display = ('title',)



admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Tag, TagAdmin)
