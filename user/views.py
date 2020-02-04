from django.shortcuts import render, redirect
import pyrebase
from .models import Contactus
import requests
import json

url = 'http://127.0.0.1:5000/files'

firebaseConfig = {
    'apiKey': "AIzaSyBc9d3c5edVlscSWzrTnMW54gI6qlI_oYA",
    'authDomain': "star-bugs.firebaseapp.com",
    'databaseURL': "https://star-bugs.firebaseio.com",
    'projectId': "star-bugs",
    'storageBucket': "star-bugs.appspot.com",
    'messagingSenderId': "450899693729",
    'appId': "1:450899693729:web:24eeb110b85b1ceaede0e0",
    'measurementId': "G-NE8B9E9EDC"
}
firebase = pyrebase.initialize_app(firebaseConfig)

authe = firebase.auth()


def index(request):
    if request.method == 'POST':
        your_name = request.POST['your_name']
        your_email = request.POST['your_email']
        your_message = request.POST['your_message']

        contact = Contactus(your_name= your_name, your_email=your_email, your_message= your_message)
        contact.save()
        return render(request,'index.html', {'message':'Your response has been recorded'})
    else:
        return render(request, 'index.html')


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = authe.sign_in_with_email_and_password(email, password)
            session_id = user['idToken']
            request.session['uid'] = str(session_id)
            return redirect('profile')


        except:
            message = 'Invalid login details'
            context = {
                'message': message
            }
            return render(request, 'login.html', context)


    else:
        return render(request, 'login.html')


def profile(request):
    try:
        idtoken = request.session['uid']
        a = authe.get_account_info(idtoken)
        b = a.get('users')
        print(b)
        print(b[0].get('email'))
        print(b[0].get('localId'))
        response = requests.get(url)
        json_response = response.json()
        print(json_response)
        l = len(json_response)
        return render(request, 'profile.html',{'gif':json_response,'loacation':'ABESIT','length':l})
    except KeyError:
        message = 'you must login first'
        return render(request,'login.html',{'message':message})



def history(request):
    try:
        idtoken = request.session['uid']
        a = authe.get_account_info(idtoken)
        return render(request, 'history.html')
    except KeyError:
        message = 'you must login first'
        return render(request,'login.html',{'message':message})


def signout(request):
    try:
        del request.session['uid']
    except KeyError:
        pass
    return redirect('login')

