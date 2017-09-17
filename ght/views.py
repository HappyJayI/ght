from django.shortcuts import render

choicecode = (
    (11, '멘트시작','musicon'),
    (10, '멘트종료','musicoff'),
    (21, '녹음시작','recordon'),
    (20, '녹음종료','recordoff'),
    (31, '조명시작','ledon'),    
    (30, '조명종료','ledoff'),    
)

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

def index2(request, pk):
    name = getChoicenamebyid(choicecode,pk)
    return render(request, 'ght/index2.html',{"name":name,"pk":pk})
