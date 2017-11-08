
from django.conf.urls import url,include
from bbs import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^category/(\d+)/$',views.category,name='category_detail'),
    url(r'^detail/(\d+)/$',views.ariticle_detail,name='article_detail'),
    url(r'^comment/$',views.comment,name='post_comment'),
    url(r'^comment_list/(\d+)/$',views.get_comments,name='get_comments'),
    url(r'^new_article/$',views.new_article,name='new-article'),
    url(r'^file_upload/$',views.file_upload,name='file-upload'),
    url(r'^latest_article_count/$',views.get_latest_article_count,name='get_latest_article_count'),
]
