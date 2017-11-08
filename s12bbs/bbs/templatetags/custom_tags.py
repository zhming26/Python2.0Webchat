from django import template
from django.utils.html import format_html  # 引入format_html模块

register = template.Library()

@register.filter
def truncate_url(img_obj): #因为使用article.head_img获得到的是headfiled对象,并不是一个字符串
    print(img_obj.name,img_obj.url) #使用.name和.url都可以获取字符串如:uploads/1133486643273333.jpeg
    return img_obj.name.split('/',maxsplit=1)[-1] #使用"/"作为分隔符,maxsplit表示只做一次分割,[-1]获取文件名

@register.simple_tag
def filter_comment(article_obj):
    query_set = article_obj.comment_set.select_related()
    comments = {
        'comment_count':query_set.filter(comment_type = 1).count(),
        'thumb_count':query_set.filter(comment_type=2).count()
    }
    return comments