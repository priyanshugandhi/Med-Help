import json
import tokenGen as token
import config
from flask import Flask,render_template
from flask import request
import nearestDoctor as nd
import forDatabase as fd
import os
import api as ap
from flask import jsonify, redirect

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)


@app.route('/')
def index():
   return render_template("index.html")

@app.route('/dashboard')
def one():
	authkey=token.getToken()
	return render_template("dashboard.html",authkey=authkey)

@app.route('/patient_information')
def two():
	authkey=token.getToken()
	return render_template("patient_information.html",authkey=authkey)

@app.route('/disease_information')
def three():
	authkey=token.getToken()
	return render_template("disease_information.html",authkey=authkey)

@app.route('/login')
def four():
   return render_template("login.html")

@app.route("/patient_submit", methods=['GET', 'POST'])
def five():
	if request.method == 'POST':
		gender=request.form['Gender']
		age=request.form["Age"]
		symptoms=request.form['ID']
		print(symptoms,age,gender)		
		authkey=token.getToken()
		return render_template("patient_information.html",authkey=authkey,gender=gender,age=age,symptoms=symptoms)


@app.route("/disease_submit", methods=['GET', 'POST'])
def six():
	if request.method == 'POST':
		issue=request.form['issue']
		authkey=token.getToken()
		return render_template("disease_information.html",authkey=authkey,issue=issue)

@app.route("/findDoctor")
def find_doctor():
	return render_template("findMyDoctor.html")

@app.route('/api/four/result', methods=['POST'])
def apiFourResult():
    data = request.get_json()
    nearestDocs = nd.nearestDoctors(data["lat"], data["long"])
    print(nearestDocs)
    nearestDocsDict = json.dumps(nearestDocs)
    return nearestDocsDict


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/uceverything',methods=['GET', 'POST'])
def upload_image():
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
		return ap.texttospeech(filename)

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

@app.route('/treatment')
def eight():
    return render_template("scrapedTreatments.html")


@app.route('/api/three/result', methods=['POST'])
def apiThreeResult():
    data = request.get_json()
    medicalConditions = fd.fetch(data["searchTerm"])
    medicalConditionsDict = json.dumps(medicalConditions)
    return medicalConditionsDict



if __name__ == '__main__':
   app.run(host='127.0.0.1',port=5001)   
