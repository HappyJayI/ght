from django.shortcuts import render
import requests
import subprocess
import os

choicecode = (
    (11, '조명시작','ledon'),
    (10, '조명종료','ledoff'),
    (21, '음악시작','musicon'),
    (20, '음악종료','musicoff'), 
)

strpath = "./ght/templates/ght/"

args = []
args.append(strpath + "ffmpeg")
args.append("-i")
args.append(strpath + "1.mp3")
args.append("-f")
args.append("s32be")
args.append("-acodec")
args.append("pcm_s32be")
args.append("-ar")
args.append("44100")
args.append("-af")
args.append("volume=0.5")
args.append("tcp://172.20.10.14:5522")

def getChoicecodebyname(choicecode,name):
    for x in choicecode:
        if x[2] == name:
            return x[0]

def getChoicenamebyid(choicecode,id):
    for x in choicecode:
        if x[0] == id:
            return x[1]

def index(request):
    return render(request, 'ght/index.html')

def led(request, pk):
    name = getChoicenamebyid(choicecode,pk)
    #return redirect("http://172.20.10.14/gpio/0")
    try:
        r = requests.get('http://172.20.10.14/gpio/%s'%str(pk))
        #pk = str(r.status_code)
    finally:
        return render(request, 'ght/index.html')

def audio(request, pk):
    name = getChoicenamebyid(choicecode,pk)
    try:
        if (pk==21):
            subprocess.Popen(args, stdout=subprocess.PIPE)
        if (pk==20):
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