from django.conf.urls import url,include
from webchat import views
urlpatterns = [
    # url(r'^$/', views.acc_login,name='login' ), 这种写法错误,r'^$/'要改成r'^$'
    url(r'^$', views.dashboard,name='chat_dashboard' ),
    url(r'^msg_send/$',views.send_msg,name='send_msg' ),
    url(r'^new_msgs/$',views.get_new_msgs,name='get_new_msgs' ),
    url(r'^file_upload/$',views.file_upload,name='file_uploads' ),
]
