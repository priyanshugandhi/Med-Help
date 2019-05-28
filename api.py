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


#url='http://192.168.43.1:8080/shot.jpg?rnd=731702'
#url='http://100.94.167.244:8080/shot.jpg?rnd=731702'
#url='http://172.18.94.110:8080/shot.jpg?rnd=731702'

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
	    ret, frame = video_capture.read()
	    #imgResp=urllib.request.urlopen(url)
	    #imgNp=np.array(bytearray(imgResp.read()),dtype=np.uint8)
	    
	    #frame=cv2.imdecode(imgNp,-1)


	    FaceFileName = "test1.jpg" #Saving the current image from the webcam for testing.
	    cv2.imwrite(FaceFileName, frame)
	    
	    try:
	        body=open(FaceFileName, "rb").read()
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


	