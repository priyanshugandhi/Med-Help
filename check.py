import http.client, urllib.request, urllib.parse, urllib.error, base64
import json
from PIL import Image
import requests
from io import BytesIO
import subprocess
from gtts import gTTS 
from pydub import AudioSegment
import numpy as np
import time
import cv2
import os
import imutils
from flask import Flask, jsonify, request, redirect

#url='http://192.168.43.1:8080/shot.jpg?rnd=731702'
#url='http://100.94.167.244:8080/shot.jpg?rnd=731702'
#url='http://172.18.94.110:8080/shot.jpg?rnd=731702'
app = Flask(__name__)

headers = {
    # Request headers
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': '1d6597318ef24ff2bed58a05479b9f18',
}

params = urllib.parse.urlencode({
    # Request parameters
    'maxCandidates': '1',
    'language': 'en',
})
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def upload_image():
	
    # Check if a valid image file was uploaded
    target = os.path.join(APP_ROOT, 'uploads/')
    print(target)
    if not os.path.isdir(target):
            os.mkdir(target)
    else:
        print("Couldn't create upload directory: {}".format(target))
    print(request.files.getlist("file"))
    
    for upload in request.files.getlist("file"):
        print(upload)
        print("{} is the file name".format(upload.filename))
        filename = upload.filename
        destination = "/".join([target, filename])
        print ("Accept incoming file:", filename)
        print ("Save it to:", destination)
        upload.save(destination)
        return texttospeech(filename)
    
    # If no valid image file was uploaded, show the file upload form:
    return '''
    <!doctype html>
    <title>UCEverything</title>
    <h1>Upload a picture!</h1>
    <form method="POST" enctype="multipart/form-data">
      <input type="file" name="file">
      <input type="submit" value="Upload">
    </form>
    '''

def texttospeech(file_stream):
	process_this_frame = True
	file_format=file_stream.split(".")
	file_names=os.listdir("uploads")
	for file in file_names:
		if file==file_stream:
			destination = "/".join(["uploads", file])
			video_capture = cv2.VideoCapture(destination) 
    

	while True:
	    # Grab a single frame of video
	    #ret, frame = video_capture.read()
	    imgResp=urllib.request.urlopen(url)
	    imgNp=np.array(bytearray(imgResp.read()),dtype=np.uint8)
	    
	    frame=cv2.imdecode(imgNp,-1)


	    FaceFileName = "test1.jpg" #Saving the current image from the webcam for testing.
	    cv2.imwrite(FaceFileName, frame)
	    
	    try:
	        body=open('/home/priyanshu/work/UCEverything/test1.jpg', "rb").read()
	        conn = http.client.HTTPSConnection('centralindia.api.cognitive.microsoft.com')
	        conn.request("POST", "/vision/v2.0/describe?%s" % params, body, headers)
	        response = conn.getresponse()
	        data = response.read()
	        print(data)
	        x=json.loads(data)
	        if x['description']['captions']==[]:
	            description="hello"
	        else:    
	            description=x['description']['captions'][0]['text']
	        tts = gTTS(description, lang='en')
	        tts.save('tts.mp3')
	        tts = AudioSegment.from_mp3("tts.mp3")
	        subprocess.call(["ffplay", "-nodisp", "-autoexit", "tts.mp3"])
	        return description
	        conn.close()
	        
	    except Exception as e:
	        print("[Errno {0}] {1}".format(e.errno, e.strerror))


if __name__ == '__main__':
   app.run(host='127.0.0.1',port=5001)   
	