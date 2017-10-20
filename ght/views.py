from django.shortcuts import render
import requests
import subprocess
import os

#client ip 설정
clientIP = {}
clientIP["Tray1"] = "192.168.0.5"
#clientIP["Tray2"] = "192.168.0.6" 
#clientIP["Tray3"] = "192.168.0.7" 

clientnames = []
for key in clientIP.keys():
    clientnames.append(key)

#조명 설정
ledcode = {}
ledcode[1] = "Basic"
ledcode[2] = "Coldwave"
ledcode[3] = "Neocandle"
ledcode[4] = "Twinkle"

ledcodenames = ledcode.values()

#streaming 설정
choicecode = (
    (11, '조명시작','ledon'),
    (10, '조명종료','ledoff'),
    (21, '음악시작','musicon'),
    (20, '음악종료','musicoff'), 
    (31, '스트림시작','streamon'),
    (30, '스트림종료','streamoff'), 
)

strpath = "./ght/templates/ght/"

streamargs = []
streamargs.append(strpath + "ffmpeg")
streamargs.append("-i")
streamargs.append(strpath + "1.mp3")
streamargs.append("-f")
streamargs.append("s32be")
streamargs.append("-acodec")
streamargs.append("pcm_s32be")
streamargs.append("-ar")
streamargs.append("44100")
streamargs.append("-af")
streamargs.append("volume=0.5")
streamargs.append("tcp://" + clientIP[clientnames[0]] + ":5522")

def index(request, clientname=clientnames[0]):
    try:
        return render(request, 'ght/index.html',{"clientnames":clientnames,"selectedclientname":clientname,\
        "ledcodenames":ledcodenames, "ledcodes":ledcode})
    finally:
        pass

def led(request, pk, clientname):
    status = ""
    try:
        r = requests.get('http://%s/gpio/%s'%(clientIP[clientname],str(pk)))    
    except requests.exceptions.HTTPError as err:
        status = err
    except requests.exceptions.RequestException as e:
        status = "클라이언트 " + clientname + " 연결이 원활하지 않습니다. 네트워크 상태를 확인해 주세요~"
    finally:
        if (status != "" ):
            return render(request, 'ght/index2.html',{"status":status})
        else:
            return index(request, clientname)

def audio(request, pk, clientname):
    status = ""
    try:
        r = requests.get('http://%s/gpio/%s'%(clientIP[clientname],str(pk)))    
    except requests.exceptions.HTTPError as err:
        status = err
    except requests.exceptions.RequestException as e:
        status = "클라이언트 " + clientname + " 연결이 원활하지 않습니다. 네트워크 상태를 확인해 주세요~"
    finally:
        if (status != "" ):
            return render(request, 'ght/index2.html',{"status":status})
        else:
            return index(request, clientname)

def audiostream(request, pk, clientname):
    try:
        if (pk==31):
            subprocess.Popen(streamargs, stdout=subprocess.PIPE)
        if (pk==30):
            #os가 windows면(nt) taskkill
            if (os.name == "nt"):
                tasklist = subprocess.Popen('tasklist /nh /fo csv /fi "IMAGENAME eq ffmpeg.exe"', stdout=subprocess.PIPE)
                out, err = tasklist.communicate()
                out = str(out)
                if (out.index('ffmpeg') > 0) :
                    subprocess.Popen('taskkill /im ffmpeg.exe /f')

            #os가 linux면(posix) kill
            else:                
                proc1 = subprocess.Popen(["ps","axg"], stdout=subprocess.PIPE)
                proc1.wait()
                proc2 = subprocess.Popen(["grep","ffmpeg"],stdin=proc1.stdout,stdout=subprocess.PIPE)
                out, err = proc2.communicate()
                out2 = out.splitlines()

                for i in out2:
                    out3 = i.split()
                    if out3[4] != "grep":
                        tasklist =  subprocess.Popen(["kill",out3[0]])   

                proc2.wait()

    finally:
        return render(request, 'ght/index.html')