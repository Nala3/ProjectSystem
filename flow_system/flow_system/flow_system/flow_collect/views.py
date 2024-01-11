from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from flow_collect.models import Pcap
import os
import time 
def index(request):
    os.system("pwd")
    name = time.asctime(time.localtime(time.time()))
    # os.system("tshark -c5 -i en0 -w ./data_raw/{}.pcap".format(str(tem).replace(" ","_")))
    pub_date = timezone.now()

    device = "enp0s31f6"
    exit_code = os.system("sudo tcpdump -c100 -i {} -w ./data_raw/{}.pcap".format(device, str(name).replace(" ","_")))
    # 查看命令的退出状态
    print(os.WEXITSTATUS(exit_code))
    tem = Pcap(name=str(name), date=pub_date)
    tem.save()
    return render(request, 'flow_collect/collect.html')
# Create your views here.
