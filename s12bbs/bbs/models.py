from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import  ValidationError #这个就是Django admin后台当出错时,抛出的红色错误提示,要自定义错误时,就得引入此方法
import datetime
# Create your models here.
# 论坛帖子表
class Article(models.Model):
    title = models.CharField(max_length=255,verbose_name=u"标题")
    brief = models.CharField(null=True,blank=True,max_length=255,verbose_name=u"描述")
    category = models.ForeignKey("Category",verbose_name=u"所属板块") #由于Category类在它的下方,所以要引号引起来,Django内部会自动反射去找
    content = models.TextField(verbose_name=u"文章内容")
    head_img = models.ImageField(verbose_name=u"文章标题图片",upload_to="uploads")
    # 默认你如果不设置upload_to,会在Django项目目录根目录下保存上传文件,此字段只存储 文件路径/文件名
    # 当我们结合前端上传文件时,也不会用upload_to 设置上传文件的保存路径,为啥不用,后面会说
    author = models.ForeignKey("UserProfile",verbose_name=u"作者")
    pub_date = models.DateField(blank=True,null=True,verbose_name=u"创建时间")
    last_modify = models.DateField(auto_now=True,verbose_name=u"修改时间")
    # 需要注意的是一旦设置auto_now=True ,默认在admin后台就是非编辑状态了,也就是在admin后台此字段为隐藏,除非手动设置可编辑属性
    # auto_now 用于修改,auto_now_add用于创建,在admin后台都是默认不可编辑(隐藏)

    priority = models.IntegerField(default=1000,verbose_name=u"优先级")
    status_choices = (('draft',u"草稿"),
                      ('published',u"已发布"),
                      ('hidden',u"隐藏"),
                    )
    status = models.CharField(max_length=64,choices=status_choices,default="published")
    def __str__(self):
        return self.title
    # django 的model类在保存数据时,会默认调用self.clean()方法的,所以可以在clean方法中定义数据的一些验证
    def clean(self):
        # 如果帖子有发布时间,就说明是发布过的帖子,发布过的帖子就不可以把状态在改成草稿状态了
        if self.status == "draft" and self.pub_date is not None:
            raise  ValidationError(u"如果你选择草稿,就不能选择发布日期!")
        # 如果帖子没有发布时间,并且保存状态是发布状态,那么就把发布日期设置成当天
        if self.status == 'published' and self.pub_date is None:
            self.pub_date = datetime.date.today()
    class Meta:
        verbose_name = u"帖子表"
        verbose_name_plural = u"帖子表"

# 评论表
class Comment(models.Model):
    article = models.ForeignKey("Article",verbose_name=u"所属文章")
    parent_comment = models.ForeignKey('self',related_name="my_clildren",blank=True,null=True,verbose_name=u"父评论")
    comment_choices = ((1,u'评论'),
                       (2,u"点赞"))
    comment_type = models.IntegerField(choices=comment_choices,default=1,verbose_name=u"评论类型")
    user = models.ForeignKey("UserProfile",verbose_name=u"评论人")
    comment = models.TextField(blank=True,null=True)
    #这里有一个问题,这里我们设置了允许为空,那就意味着我们在页面上点了评论,却又没有输入内容,这样岂不是很不合理.那么怎么实现只要你点了评论,内容就不能为空.
    # 那么我们会问,为什么允许为空,直接不为空就好了.因为我们这里把评论和点赞放到了一张表中,当为点赞时,当然就不需要评论内容了.所以可以为空.
    # 我们会想在前端进行判断或者在views写代码进行判断,这里告诉你这里我们就可以实现这个限制.使用Django中clean()方法,models类在保存之前它会调用self.clean方法,所以我们可以在这里定义clean方法,进行验证
    date = models.DateTimeField(auto_now_add=True,verbose_name=u"评论时间")

    def clean(self):
        # 如果comment的状态为评论,那么评论内容就不能为空
        if self.comment_type ==1 and len(self.comment)==0:
            raise ValidationError(u"评论内容不能为空")
        # 我想知道这个报错显示在什么位置,我们看到每一个字段有报错,也只是显示在form表单的字段上,这里做了判断错误信息会显示在什么地方?
        # 后面把错误信息显示的位置截图展示
    def __str__(self):
        return "%s,P:%s,%s"%(self.article,self.parent_comment_id,self.comment)

    class Meta:
        verbose_name = u"评论表"
        verbose_name_plural = u"评论表"
# 板块表
class Category(models.Model):
    name = models.CharField(max_length=64,unique=True,verbose_name=u"板块名称") #unique是否唯一
    brief = models.CharField(null=True,blank=True,max_length=255,verbose_name=u"描述")
    set_as_top_menu = models.BooleanField(default=False,verbose_name=u"是否将此板块设置在页面顶部")
    positon_index = models.SmallIntegerField(verbose_name=u"顶部展示的位置")
    admins = models.ManyToManyField("UserProfile",blank=True,verbose_name=u"版主")
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = u"板块表"
        verbose_name_plural = u"板块表"

from django.contrib.auth.models import User
# 用户表继承Django里的User
class UserProfile(models.Model):
    user = models.OneToOneField(User,verbose_name=u"关联Django内部的用户")
    name = models.CharField(max_length=32,verbose_name=u"昵称")
    signature = models.CharField(max_length=255,blank=True,null=True,verbose_name=u"签名")
    # head_img = models.ImageField(height_field='150',width_field='150',blank=True,null=True,verbose_name=u"头像",upload_to="uploads")
    head_img = models.ImageField(blank=True,null=True,verbose_name=u"头像",upload_to="uploads")
    #ImageFied字段说明https://docs.djangoproject.com/en/1.9/ref/models/fields/
    #大概的意思是,ImageField 继承的是FileField,除了FileField的属性被继承了,它还有两个属性 ImageField.height_field和ImageField.width_field,设置后当你存入图片字段时,它会把默认尺寸设置成高height_field宽:width_field
    # 如果想在前端上传图像,需要下载一个Pillow模块,具体使用后面会用到
    friends = models.ManyToManyField('self',related_name='my_friends',blank=True)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u"用户表"
        verbose_name_plural = u"用户表"

# 用户组表,其实这里用不到,因为我们使用Django的 User,
class UserGroup(models.Model):
    pass