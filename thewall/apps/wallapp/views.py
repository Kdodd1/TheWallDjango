from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User, Message, Comment
import bcrypt

def index(request):
	request.session.clear()
	return render(request, "wallapp/index.html")

def create(request):
	errors = User.objects.basic_validator(request.POST)
	if len(errors):
		for key, value in errors.items():
			messages.add_message(request, messages.ERROR, value, extra_tags='register')
		return redirect('/')
	else:
		password = request.POST['password']
		password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
		User.objects.create(first_name= request.POST['first_name'], last_name = request.POST['last_name'], email= request.POST['email'], password= password)
		request.session['email'] = request.POST['email']
		request.session['user_id'] = User.objects.get(email= request.POST['email']).id 
	return redirect('/logged')

def login(request):
	errors = User.objects.login_validator(request.POST)
	if len(errors):
		for key, value in errors.items():
			messages.add_message(request, messages.ERROR, value, extra_tags= "login")
		return redirect('/')
	else: 
		request.session['email'] = request.POST['email_log']
		request.session['user_id'] = User.objects.get(email= request.POST['email_log']).id 

	return redirect('/logged')

def logged(request):
	if 'user_id' not in request.session:
		return redirect('/')
	else:
		content = {
			"messages" : Message.objects.all(),
			"comments" : Comment.objects.all()
			}

		return render(request, 'wallapp/logged.html', content)

def message(request):
	Message.objects.create(message= request.POST['message'], user_id= request.POST['user_id'])
	return redirect('/logged')

def comment(request):
	Comment.objects.create(comment= request.POST['comment'], user_id=request.session['user_id'], messages_id= request.POST['message_id'])
	print("create comment")
	return redirect('/logged')

def deletemessage(request, messageid):
	message = Message.objects.get(id = messageid)
	message.delete()
	return redirect('/logged')

def deletecomment(request, commentid):
	comment = Comment.objects.get(id = commentid)
	comment.delete()
	return redirect('/logged')
