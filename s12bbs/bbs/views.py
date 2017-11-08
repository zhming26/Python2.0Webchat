from django.shortcuts import render,HttpResponse,HttpResponseRedirect,redirect
from bbs import models
from django.contrib.auth.decorators import login_required  # login_required 这是装饰器函数
from django.contrib.auth import authenticate,login,logout
import json
from bbs import comment_hander
from bbs import forms

# Create your views here.

category_list = models.Category.objects.filter(set_as_top_menu =True).order_by('positon_index')

def index(request):
    print(category_list)
    category_obj = models.Category.objects.get(positon_index=1)
    article_list = models.Article.objects.filter(status='published')
    return render(request,"bbs/index.html",{'category_list':category_list,
                                            'category_obj':category_obj,
                                            'article_list':article_list})
    # return HttpResponse("OK")

def category(request,id):
    category_obj = models.Category.objects.get(id=id)
    if category_obj.positon_index == 1: #我们把板块"全部"认定为首页显示,把所有的文章都显示出来,首页就认定当position_index 为1时既是首页.
        article_list = models.Article.objects.filter(status='published')
    else:
        article_list = models.Article.objects.filter(category_id = category_obj.id,status='published')
    return render(request,"bbs/index.html",{'category_list':category_list,
                                            'category_obj':category_obj,
                                            'article_list':article_list})

def acc_logout(request):
    logout(request)
    return HttpResponseRedirect('/bbs/')

def acc_login(request):
    if request.method == 'POST':
        user = authenticate(username = request.POST.get('username'),
                            password = request.POST.get('password'))
        if user is not None:
            login(request,user)
            # return redirect('/bbs/')
            return HttpResponseRedirect(request.GET.get('next') or '/bbs/')
        else:
            login_err = 'Wrong username or password'
            return render(request,'login.html',{'login_err':login_err})
    else:
        return render(request,'login.html')

# 定义文章明细页面的视图函数
def ariticle_detail(request,id):
    ariticle_obj = models.Article.objects.get(id = id)
    comment_tree = comment_hander.build_tree(ariticle_obj.comment_set.select_related())  #在这里将这片文章所有的评论传给build_tree函数,生成一个有层级关系的字典
    return render(request,'bbs/article_detail.html',{'article_obj':ariticle_obj,'category_list':category_list})

def comment(request):
    print(request.POST)
    if request.method == 'POST':
        new_comment_obj = models.Comment(

            article_id = request.POST.get('article_id'),
            parent_comment_id = request.POST.get('parent_commet_id' or None),
            comment_type = request.POST.get("comment_type"),
            user_id = request.user.userprofile.id,
                #这里要主要,我们在bbs系统用户验证用的是Django自带的用户验证模块,经过验证的用户其实是admin的后台账户,我们在前台是userprofile和admin的user做了1对1的外键关联.
                #所以这里是 request.user.userprofile.id而不是request.userprofile.id
            comment = request.POST.get('comment'),
        )
        new_comment_obj.save()
    return HttpResponse('post-comment-success')

def get_comments(request,article_id):
    article_obj = models.Article.objects.get(id=article_id)
    comment_tree = comment_hander.build_tree(article_obj.comment_set.select_related())
    tree_html = comment_hander.render_comment_tree(comment_tree)
    return HttpResponse(tree_html)

@login_required(login_url='/login/')
def new_article(request):
    if request.method=="GET":
        article_form = forms.ArticleModelForm() #实例化form类
        return render(request,'bbs/new_article.html',{'article_form':article_form,})
    elif request.method == 'POST':
        print(request.POST)
        print(request.FILES)
        article_form = forms.ArticleModelForm(request.POST,request.FILES)
        if article_form.is_valid():
            data = article_form.cleaned_data
            data['author_id'] = request.user.userprofile.id
            article_obj = models.Article(**data)
            article_obj.save()
            # article_form.save()
        else:
            return render(request,'bbs/new_article.html',{'article_form':article_form,})
        return HttpResponse('创建成功')

def file_upload(request):
    print(request.FILES)
    file_obj = request.FILES.get('filename')

    with open('uploads/%s'%file_obj.name,'wb+') as destination:

        for chunk in file_obj.chunks():

            destination.write(chunk)

    return render(request,'bbs/new_article.html')

def get_latest_article_count(request):

    latest_article_id = request.GET.get("latest_id")

    new_article_count = models.Article.objects.filter(id__gt=latest_article_id).count()

    # print("new article count:",new_article_count)

    return HttpResponse(json.dumps({'new_article_count':new_article_count}))
