# @Django packages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import JsonResponse
from django.shortcuts import render, redirect

# @Packages
import openai
from dotenv import dotenv_values

# @Scripts
from .models import Chat

config = dotenv_values(".env")
openai.api_key = config.get('OPENAI_API_KEY')

def ask_openai(message):
  response = openai.Completion.create(
    model="text-ada-001",
    prompt = message,
    n=1,
    max_tokens=150,
    stop=None,
    temperature=0.7,
  )
  answer = response.choices[0].text.strip()
  return answer

@login_required(login_url="/login")
def chatbot(request):
  chats = Chat.objects.filter(user=request.user)
  if request.method == 'POST':
    message = request.POST.get('message')
    response = ask_openai(message)

    chat = Chat(user=request.user, message=message, response=response)
    chat.save()
    return JsonResponse({'message': message , 'response': response})
  return render(request, 'chatbot.html', {'chats': chats})

def login(request):
  if request.method == 'POST':
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = auth.authenticate(request, username=username, password=password)
    if user is not None:
      auth.login(request, user)
      return redirect('chatbot')
    else:
      error_message = 'Invalid username or password'
      return render(request, 'login.html', {'error_message': error_message})
  else:
    return render(request, "login.html")

def register(request):
  if request.method == 'POST':
    username = request.POST['username'] # victor
    email = request.POST['email'] # vz@hotmail.com
    password1 = request.POST['password1'] # 1234
    password2 = request.POST['password2'] # 1234

    if password1 == password2:
      try:
        user = User.objects.create_user(username, email, password1)
        user.save()
        auth.login(request, user)
        return redirect('chatbot')
      except:
        error_message = 'Error creating account'
        return render(request, 'register.html', {'error_message': error_message})
    else:
      error_message = 'Password don\'t match'
      return render(request, 'register.html', {'error_message': error_message})

  return render(request, "register.html")

def logout(request):
  auth.logout(request)
  return redirect('login')
