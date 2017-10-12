import os
import subprocess

if (os.name == "nt"):
    tasklist = subprocess.Popen('tasklist /nh /fo csv /fi "IMAGENAME eq ffmpeg.exe"', stdout=subprocess.PIPE)
    out, err = tasklist.communicate()
    out = str(out)
    if (out.index('ffmpeg') > 0) :
        subprocess.Popen('taskkill /im ffmpeg.exe /f')

#os가 linux면 kill
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