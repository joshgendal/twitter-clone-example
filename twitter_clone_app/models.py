from django.db import models
from django.db.models.fields.related import ForeignKey
import bcrypt, re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
  def registration_val(self, post_data):
    errors = {}
    if not EMAIL_REGEX.match(post_data['email']):
      errors['email'] = 'Email is not valid'
    if post_data['password'] != post_data['confirm_password']:
      errors['password'] = 'Passwords do not match'
    return errors
  def authenticate(self, email, password):
    users = self.filter(email=email)
    if not users:
      return False
    user = users[0]
    return bcrypt.checkpw(password.encode(), user.password.encode())

class User(models.Model):
  first_name = models.CharField(max_length=45)
  last_name = models.CharField(max_length=45)
  email = models.EmailField(unique=True)
  password = models.CharField(max_length=255)
  created_at = models.DateTimeField(auto_now_add=True, null=True)
  updated_at = models.DateTimeField(auto_now=True, null=True)

  objects = UserManager()

  def __str__(self):
    return f"{self.first_name} {self.last_name} {self.email}"

class TweetManager(models.Manager):
  def validate_tweet(self, text):
    errors = {}
    if len(text) < 2:
      errors['length'] = 'Tweet must be at least 2 characters'
    if len(text) > 280:
      errors['length'] = 'Tweet can be max of 280 characters'
    return errors

class Tweet(models.Model):
  text = models.CharField(max_length=280)
  user = models.ForeignKey(User, related_name="tweets", on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True, null=True)
  updated_at = models.DateTimeField(auto_now=True, null=True)

  objects = TweetManager()

class Comment(models.Model):
  text = models.CharField(max_length=280, null=True)
  user = ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
  tweet = ForeignKey(Tweet, related_name="comments", on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True, null=True)
  updated_at = models.DateTimeField(auto_now=True, null=True)