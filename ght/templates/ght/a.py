import subprocess

args = []
args.append("ffmpeg")
args.append("-i")
args.append("1.mp3")
args.append("-f")
args.append("s32be")
args.append("-acodec")
args.append("pcm_s32be")
args.append("-ar")
args.append("44100")
args.append("-af")
args.append("volume=0.5")
args.append("tcp://172.20.10.14:5522")

subprocess.Popen(args, stdout=subprocess.PIPE)