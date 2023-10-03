from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, NewPost, Comment


class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'password', 'image', 'first_name', 'last_name', 'dob', 'phonenumber']
    search_fields = ['username', 'email']    
admin.site.register(User, CustomUserAdmin)



class NewPostAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'content', 'created_at']  
admin.site.register(NewPost, NewPostAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'content', 'created_at']  
admin.site.register(Comment, CommentAdmin)

