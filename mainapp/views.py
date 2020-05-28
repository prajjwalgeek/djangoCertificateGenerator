from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.conf.urls.static import static



from PIL import Image, ImageDraw, ImageFont
import pyfastcopy
import shutil
import os
from uuid import uuid4
import pandas as pd


# Create your views here.
def home(request):
    if request.method == 'POST':
        print("made a post")
        return HttpResponse('done')

        #to get the POST request through HTML name property we use below
        # print(request.POST.get('name'))
        template= request.FILES['template']
        data = request.FILES['data']
        fs = FileSystemStorage()
        #clear concept this with documentation
        templateName = fs.save(template.name, template)
        template_url = fs.url(templateName)
        dataName = fs.save(data.name, data)
        data_url = fs.url(dataName)

        # log=open(getAbsolutePath('uploadedFiles/log.csv'),'w')
        # # file = open("/Users/PrajjwalMishra/Documents/certificateGenerator/files/in.csv","r")
        
        # #converting to list with pandas     
        # data = pd.read_csv(getAbsolutePath('uploadedFiles/in.csv'))
        # names = data['Name'].to_list()
        # template = getAbsolutePath('uploadedFiles/BASE.jpg')
        # generateCertificate(template, names, log)
        # print(getAbsolutePath(data_url))

        template_open = os.path.join(settings.BASE_DIR,os.path.join('uploadedFiles/',template.name))
        data_open = os.path.join(settings.BASE_DIR,os.path.join('uploadedFiles/',data.name))

        generateCertificate(template_open,data_open)
        return render(request,'mainapp/index.html',{
            'templateURL':template_url,
            'dataURL': data_url,
        })
    else:
        return render(request,'mainapp/index.html')

def generateCertificate(templateDIR, data_url):

    # data = pd.read_csv(getAbsolutePath(data_url))
    data = pd.read_csv(data_url)
    data = data['Name'].to_list()
    print("========================GENERATING CERTIFICATES========================")
    sessionID = id = str(uuid4())[:8]
    os.mkdir(os.path.join(settings.BASE_DIR,os.path.join('Output/',sessionID)))
        
    for x in data:
        # base = Image.open(templateDIR)
        base = openFile(templateDIR)
        
        #.size gets size of the certificate base file (base) in width, height
        W,H=base.size
        #https://kite.com/python/answers/how-to-get-the-size-of-an-image-with-pil-in-python

        putText=ImageDraw.Draw(base)
        
        font1=ImageFont.truetype(getAbsolutePath('files/tahoma.ttf'), 40)
        font2=ImageFont.truetype(getAbsolutePath('files/tahoma.ttf'),10)

        print("done till here")
        text=str(x) #name of child
        text=text.title() #converting to Title Case
        if text == "":
            continue
        id = str(uuid4())[:8]

        #TERMINAL TEMP MESSAGES
        # print(".", end = ' ')
        print(text, end = ' ')
        print("\twith ID" + id)

        #get size of the certificate text
        w,h = putText.textsize(text, font=font1)
        # print(((W-w)/2,(H-h-25)/2))
        #putText adjustment :- number for moving text vertically. h negative goes up positive goes down
        putText.text(((W-w)/2,(H-h-35)/2), text, fill="black",font=font1) 
        putText.text(((W-W+20)/2,(H-20)),("CERTIFICATION ID : BINARY_%s"%id) , fill="#ffff",font=font2)
        base.save("TEMP_CERT.png",'PNG')
        shutil.copy("TEMP_CERT.png","Output/"+sessionID+"/"+id+".png")
        # log.write(id+","+text+"\n")
    os.remove("TEMP_CERT.png")


def getAbsolutePath(relativePath):
    pwdPath = os.getcwd()
    absolutePath = os.path.join(pwdPath, relativePath)
    return absolutePath


def openFile(filePath):
    try:
        return Image.open(filePath)
    except FileNotFoundError:
        print("template file not found")
        exit(0)