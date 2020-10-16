from django.shortcuts import render,get_object_or_404,HttpResponseRedirect
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build
from oauth2client import file, client, tools
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import json
import requests
import os

def sheet(request):
	if request.method == "POST":
		# use creds to create a client to interact with the Google Drive API
		scope = ['https://spreadsheets.google.com/feeds',
				 'https://www.googleapis.com/auth/drive',
				 'https://www.googleapis.com/auth/drive.file',
				 'https://www.googleapis.com/auth/drive.appdata',
				 'https://www.googleapis.com/auth/drive.apps.readonly']
		
		creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
		client = gspread.authorize(creds)

		service = build('drive', 'v3', credentials=creds)
		# Find a workbook by name and open the first sheet
		# Make sure you use the right name here.
		sheet = client.open("task-drive@task-292517.iam.gserviceaccount.com").sheet1

		Name = request.POST['name']
		Email = request.POST['email']
		Mobile_No = request.POST['mobileno']
		Messages = request.POST['message']
		Attachment_File = request.FILES.getlist("filename")

		#here form data storing like name, email, mobile_no, message
		row = [Name, Email, Mobile_No,	Messages]
		index = 2
		sheet.insert_row(row, index)
		for filename in Attachment_File:
			#file uploading code
			path = default_storage.save(filename.name, ContentFile(filename.read()))
			headers = {"Authorization": "Bearer ## enter user access_token ##"}
			para = {
			    "name": filename.name,
			    "parents": [folder_id]
			}
			files = {
			    'data': ('metadata', json.dumps(para), 'application/json; charset=UTF-8'),
			    'file': open(os.path.join(settings.MEDIA_ROOT, path), "rb")
			}
			r = requests.post(
			    "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
			    headers=headers,
			    files=files
			)
			# print(r.text)
		messages.success(request, 'Thank you for submission form')
	return render(request, 'contactus.html', {"Messages":"data not stored"})
