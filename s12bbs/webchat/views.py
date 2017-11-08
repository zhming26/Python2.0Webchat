from django.shortcuts import render,HttpResponse
from django.contrib.auth.decorators import  login_required
import json,queue,time
from webchat import models
# Create your views here.

GLOBAL_MSG_QUEUES={

}
@login_required
def dashboard(request):
    # return HttpResponse('ok')
    return render(request,'webchat/dashboard.html')

@login_required
def send_msg(request):
    print(request.POST)
    msg_data = request.POST.get('data')
    if msg_data:
        msg_data = json.loads(msg_data)
        msg_data['timestamp'] = time.time()
        if msg_data['type'] == 'single':
            if not GLOBAL_MSG_QUEUES.get(int(msg_data['to'])):
                GLOBAL_MSG_QUEUES[int(msg_data['to'])] = queue.Queue()
            GLOBAL_MSG_QUEUES[int(msg_data['to'])].put(msg_data)
        else: #group
            #找到这个组里的所有成员,把发给该组的消息发给所有成员
            group_obj = models.WebGroup.objects.get(id = int(msg_data['to']))

            for member in group_obj.members.select_related():
                if not GLOBAL_MSG_QUEUES.get(member.id):
                    GLOBAL_MSG_QUEUES[member.id] = queue.Queue()
                if member.id != request.user.userprofile.id:
                    GLOBAL_MSG_QUEUES[member.id].put(msg_data)

    print(GLOBAL_MSG_QUEUES)
    return HttpResponse("---msg recevied---")

def get_new_msgs(request):
    # 先判断自己有没有queue,如果是新用户第一次登录就是没有queue
    if request.user.userprofile.id not in GLOBAL_MSG_QUEUES:
        print("no queue for user[%s]"%request.user.userprofile.id,request.user)
        GLOBAL_MSG_QUEUES[request.user.userprofile.id] = queue.Queue() #创建一个queue
    msg_count = GLOBAL_MSG_QUEUES[request.user.userprofile.id].qsize() #获取queue的大小
    q_obj = GLOBAL_MSG_QUEUES[request.user.userprofile.id]
    msg_list = []
    if msg_count > 0:
        for msg in range(msg_count):
            msg_list.append(q_obj.get()) #q_obj.get()不需要指定参数,会找最旧的那一条
        print("new msgs:",msg_list)
    else:#没消息,要挂起
        print(GLOBAL_MSG_QUEUES)
        try:
            msg_list.append(q_obj.get(timeout=60)) #如果有消息,则立刻加入到msg_list列表,如果超时进入except
        except queue.Empty:     #如果列表为空,打印下面消息
            print("\033[41;1mno msg for [%s][%s]\033[0m"%(request.user.userprofile.id,request.user))
    return HttpResponse(json.dumps(msg_list))


def file_upload(request):
    print(request.POST,request.FILES)
    file_obj = request.FILES.get('file')
    new_file_name = "uploads/%s"%file_obj.name
    with open(new_file_name,"wb+") as new_file_obj:
        for chunk in file_obj.chunks():
            new_file_obj.write(chunk)
    return HttpResponse('--upload success---')