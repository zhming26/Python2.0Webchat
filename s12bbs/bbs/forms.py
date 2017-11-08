#_*_coding:utf-8_*_
__author__ = 'ZhouMing'

from django.forms import Form,ModelForm
from bbs import models

class ArticleModelForm(ModelForm):
    class Meta:
        model = models.Article
        exclude = ('author','pub_date','priority',)

    # 先继承,再重写(想重新定义某些字段的属性,必须先继承,在重写,就这样记着)
    def __init__(self,*args,**kwargs):
        super(ArticleModelForm,self).__init__(*args,**kwargs)
        # self.fields['qq'].widget.attrs["class"] = "form-control"

        # for循环每一个字段,修改字段的class属性
        for field_name in self.base_fields:      #self.base_fields说白了就是把所有字段取出来但是是字典的形势
            field = self.base_fields[field_name]
            #这里可以是上面的例子field.widget.attrs["class"] = "form-control",也可以用update,用update的好处就是可以同时修改多个属性了
            field.widget.attrs.update({'class':"form-control"})