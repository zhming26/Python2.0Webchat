from django.contrib import admin
from bbs import models
# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title','category','author','pub_date','last_modify','status')
class CommentAdmin(admin.ModelAdmin):
    list_display = ('article','parent_comment','comment_type','comment','user')
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','set_as_top_menu','positon_index',)


admin.site.register(models.Article,ArticleAdmin)
admin.site.register(models.Comment,CommentAdmin)
admin.site.register(models.Category,CategoryAdmin)
admin.site.register(models.UserProfile)