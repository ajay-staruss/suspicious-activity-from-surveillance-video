from django.shortcuts import render, redirect
import pyrebase
from django.contrib import auth

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
    return render(request, 'index.html')


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = authe.sign_in_with_email_and_password(email, password)
            session_id = user['idToken']
            request.session['uid'] = str(session_id)
            return render(request, 'profile.html', {'e': email})


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
        print(b[0].get('email'))
        return render(request, 'profile.html')
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
