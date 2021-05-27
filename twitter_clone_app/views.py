from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import *
import bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
print(EMAIL_REGEX.match('jgendalcodingdojocom'))

fake_pw = 'codingisfun123'
hash_pw = bcrypt.hashpw(fake_pw.encode(), bcrypt.gensalt()).decode()
print('password is', fake_pw, 'hash is', hash_pw)

# Create your views here.
def index(request):
  return render(request, 'index.html')

def register(request):
  if request.method == "POST":
    errors = User.objects.registration_val(request.POST)
    if len(errors) > 0:
      for key, val in errors.items():
        messages.error(request, val)
      return redirect("/")
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']
    password = request.POST['password']
    # hash pw w/ bcrypt
    hash_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    User.objects.create(first_name=first_name, last_name=last_name, email=email, password=hash_pw)
  return redirect('/')

def login(request):
  if request.method == "POST":
    email = request.POST['email']
    password = request.POST['password']
    if not User.objects.authenticate(email, password):
      messages.error(request, 'EMail and password dont match')
      return redirect('/')
    user = User.objects.get(email=email)
    request.session['user_id'] = user.id
    return redirect("/tweet")
  return redirect('/')

def logout(request):
  del request.session['user_id']
  return redirect("/")
# protected route
def tweet(request):
  if 'user_id' not in request.session:
    return HttpResponse("<h1>You must be logged in to get to the tweet page</h1>")
  user = User.objects.get(id=request.session['user_id'])
  context = {
    "user": user
  }
  return render(request, 'tweet.html', context)

def add_tweet(request):
  if request.method == "POST":
    text = request.POST['tweet_text']
    user = User.objects.get(id=request.session['user_id'])
    errors = Tweet.objects.validate_tweet(text)
    if len(errors) > 0:
      # blah
      for key, val in errors.items():
        messages.error(request, val)
      return redirect('/tweet')
    Tweet.objects.create(text=text, user=user)
    return redirect("/feed")

def feed(request):
  all_tweets = Tweet.objects.all()
  context = {
    "all_tweets": all_tweets
  }
  return render(request, 'feed.html', context)

def edit_tweet_template(request, tweet_id):
  if 'user_id' not in request.session:
    return HttpResponse("<h1>You must be logged in to edit a tweet!</h1>")
  tweet = Tweet.objects.get(id=tweet_id)
  context = {
    "tweet": tweet
  }
  return render(request, 'edit_tweet.html', context)

def edit_tweet(request):
  if request.method == "POST":
    tweet_id = request.POST['tweet_id']
    text = request.POST['tweet_text']
    errors = Tweet.objects.validate_tweet(text)
    if len(errors) > 0:
      for key, val in errors.items():
        messages.error(request, val)
      return redirect(f"/edit-tweet/{ request.POST['tweet_id'] }")
    tweet_to_edit = Tweet.objects.get(id=tweet_id)
    tweet_to_edit.text = text
    tweet_to_edit.save()
    return redirect("/feed")

def add_comment(request):
  if request.method == "POST":
    tweet_id = request.POST['tweet_id']
    comment_text = request.POST['comment_text']
    tweet = Tweet.objects.get(id=tweet_id)
    user = User.objects.get(id=request.session['user_id'])
    Comment.objects.create(text=comment_text, tweet=tweet, user=user)
    return redirect('/feed')
