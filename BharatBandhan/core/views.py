from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Profile, Post, LikePost, FollowersCount, CustomerProfile
from itertools import chain
import random
from django.http import JsonResponse

# Create your views here.

@login_required(login_url='signin')
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    user_following_list = []
    feed = []

    user_following = FollowersCount.objects.filter(follower=request.user.username)

    for users in user_following:
        user_following_list.append(users.user)

    for usernames in user_following_list:
        feed_lists = Post.objects.filter(user=usernames)
        feed.append(feed_lists)

    feed_list = list(chain(*feed))

    # user suggestion starts
    all_users = User.objects.all()
    user_following_all = []

    for user in user_following:
        user_list = User.objects.get(username=user.user)
        user_following_all.append(user_list)
    
    new_suggestions_list = [x for x in list(all_users) if (x not in list(user_following_all))]
    current_user = User.objects.filter(username=request.user.username)
    final_suggestions_list = [x for x in list(new_suggestions_list) if ( x not in list(current_user))]
    random.shuffle(final_suggestions_list)

    username_profile = []
    username_profile_list = []

    for users in final_suggestions_list:
        username_profile.append(users.id)

    for ids in username_profile:
        profile_lists = Profile.objects.filter(id_user=ids)
        username_profile_list.append(profile_lists)

    suggestions_username_profile_list = list(chain(*username_profile_list))


    return render(request, 'index.html', {'user_profile': user_profile, 'posts':feed_list, 'suggestions_username_profile_list': suggestions_username_profile_list[:4]})

@login_required(login_url='signin')
def upload(request):

    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']

        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()

        return redirect('/')
    else:
        return redirect('/')

@login_required(login_url='signin')
def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    if request.method == 'POST':
        username = request.POST['username']
        username_object = User.objects.filter(username__icontains=username)

        username_profile = []
        username_profile_list = []

        for users in username_object:
            username_profile.append(users.id)

        for ids in username_profile:
            profile_lists = Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)
        
        username_profile_list = list(chain(*username_profile_list))
    return render(request, 'search.html', {'user_profile': user_profile, 'username_profile_list': username_profile_list})

@login_required(login_url='signin')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id)

    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()

    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_likes = post.no_of_likes+1
        post.save()
        return redirect('/')
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes-1
        post.save()
        return redirect('/')

@login_required(login_url='signin')
def profile(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=pk)
    user_post_length = len(user_posts)

    follower = request.user.username
    user = pk

    if FollowersCount.objects.filter(follower=follower, user=user).first():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'

    user_followers = len(FollowersCount.objects.filter(user=pk))
    user_following = len(FollowersCount.objects.filter(follower=pk))

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_length': user_post_length,
        'button_text': button_text,
        'user_followers': user_followers,
        'user_following': user_following,
    }
    return render(request, 'profile.html', context)

@login_required(login_url='signin')
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']

        if FollowersCount.objects.filter(follower=follower, user=user).first():
            delete_follower = FollowersCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect('/profile/'+user)
        else:
            new_follower = FollowersCount.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect('/profile/'+user)
    else:
        return redirect('/')

@login_required(login_url='signin')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        
        if request.FILES.get('image') == None:
            image = user_profile.profileimg
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        
        return redirect('settings')
    return render(request, 'setting.html', {'user_profile': user_profile})

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        print(username)
        print(get_response(username))
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                #log user in and redirect to settings page
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                #create a Profile object for the new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('settings')
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('signup')
        
    else:
        return render(request, 'signup.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('signin')

    else:
        return render(request, 'signin.html')

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')

def Findex(request):
  if request.method == 'POST':
    message = request.POST.get('message')
    if message:
      # Process user message (call get_response or your chatbot logic)
      response = get_response(message)  # Replace with your logic
      messages = [{'sender': 'bot', 'content': response}]
  else:
    messages = []
  return render(request, 'Findex.html', {'messages': messages})

def send_message(request):
    if request.method == 'POST':
        message = request.POST['message']
        response = get_response(message)
        return JsonResponse({'response': response})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

def Fsignup(request):
    # Signup using Name, Email, Document, Password
    if request.method == 'POST':
        name = request.POST['name']
        print(get_response(name))
        email = request.POST['email']
        document = request.POST['file']  # Assuming you'll handle document processing elsewhere
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('Fsignup')
            elif User.objects.filter(username=name).exists():
                messages.info(request, 'Username Taken')
                return redirect('Fsignup')
            else:
                user = User.objects.create_user(username=name, email=email, password=password)
                user.save()

                # Log user in and redirect to settings page
                user_login = auth.authenticate(username=name, password=password)
                auth.login(request, user_login)

                # Create a CustomerProfile object for the new user
                customer_profile = CustomerProfile.objects.create(
                    user=user,
                    name=name,  # Populate other fields as needed
                    email=email,  # If you want to store email in both models
                    # ... other fields from the CustomerProfile model
                )
                customer_profile.save()
                return redirect('Findex')
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('Fsignup')
    else:
        return render(request, 'Fsignup.html')
   
def Fsignin(request):
    if(request.method == 'POST'):
        customer_ID = request.POST['cust_ID']
        password = request.POST['password']
        return redirect('Ftransaction')
        
    return render(request, 'Fsignin.html')

def Flogout(request):
    return render(request, 'Flogout.html')

def Fhomepage(request):
    return render(request, 'Fhomepage.html')

def Fprofile(request):
    return render(request, 'Fprofile.html')

def Fdocuments(request):
    return render(request, 'Fdocuments.html')

def Floan(request):
    return render(request, 'Floan.html')

def Fnetbanking(request):
    return render(request, 'Fnetbanking.html')

def Fdeposit(request):
    return render(request, 'Fdeposit.html')


def Ftransaction(request):
    if request.method == 'POST':
        # Get form data
        account_holder = request.POST.get('account-holder')
        receiver = request.POST.get('receiver')
        payment_type = request.POST.get('payment-type')
        amount = request.POST.get('amount')

        # Create a new CustomerProfile object (assuming no authentication)
        customer_profile = CustomerProfile(
            cust_acc_num=account_holder,
            rec_acc_num=receiver,
            account_type=payment_type,
            cust_old_bal=10000,  # Assuming initial balance
            cust_new_bal=10000 - float(amount),  # Update balance after transaction
            rec_old_bal=10000,  # Assuming initial balance
            rec_new_bal=10000
        )
        customer_profile.save()
    return render(request, 'Ftransaction.html')

# ChatBot
# import random
# import json
# import torch
# from core.model import NeuralNet
# from core.nltk_utils import bag_of_words, tokenize
# from googletrans import Translator

# device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# with open('core/intents.json', 'r') as json_data:
#     intents = json.load(json_data)

# FILE = "core/data.pth"
# data = torch.load(FILE)

# input_size = data["input_size"]
# hidden_size = data["hidden_size"]
# output_size = data["output_size"]
# all_words = data['all_words']
# tags = data['tags']
# model_state = data["model_state"]

# model = NeuralNet(input_size, hidden_size, output_size).to(device)
# model.load_state_dict(model_state)
# model.eval()

# translator = Translator()

# bot_name = "Sam"

# def translate_to_english(text):
#     translated = translator.translate(text, dest='en')
#     return translated.text

# def translate_to_original_language(text, dest_language):
#     translated = translator.translate(text, dest=dest_language)
#     return translated.text

# def get_response(msg):
#     # Check if the message is in English, if not, translate it to English
#     detected_language = translator.detect(msg).lang
#     if detected_language != 'en':
#         msg = translate_to_english(msg)

#     sentence = tokenize(msg)
#     X = bag_of_words(sentence, all_words)
#     X = X.reshape(1, X.shape[0])
#     X = torch.from_numpy(X).to(device)

#     output = model(X)
#     _, predicted = torch.max(output, dim=1)

#     tag = tags[predicted.item()]

#     probs = torch.softmax(output, dim=1)
#     prob = probs[0][predicted.item()]
#     if prob.item() > 0.75:
#         for intent in intents['intents']:
#             if tag == intent["tag"]:
#                 response = random.choice(intent['responses'])
#                 # Translate response back to the original language if needed
#                 if detected_language != 'en':
#                     response = translate_to_original_language(response, detected_language)
#                 return response
    
#     return "I do not understand..."

import random
import json
import torch
from core.model import NeuralNet
from core.nltk_utils import bag_of_words, tokenize
from googletrans import Translator


import google.generativeai as genai
GOOGLE_API_KEY="AIzaSyClDQFt4Nr5QHnbQtk7nnq6v6ORHVy4VNI"
genai.configure(api_key=GOOGLE_API_KEY)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('core/intents.json', 'r') as json_data:
    intents = json.load(json_data)

FILE = "core/data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

translator = Translator()

bot_name = "Sam"

def translate_to_english(text):
    translated = translator.translate(text, dest='en')
    return translated.text

def translate_to_original_language(text, dest_language):
    translated = translator.translate(text, dest=dest_language)
    return translated.text

def get_response(msg):
    # Check if the message is in English, if not, translate it to English
    detected_language = translator.detect(msg).lang
    if detected_language != 'en':
        msg = translate_to_english(msg)

    sentence = tokenize(msg)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                response = random.choice(intent['responses'])
                # Translate response back to the original language if needed
                if detected_language != 'en':
                    response = translate_to_original_language(response, detected_language)
                return response
    
    model1 = genai.GenerativeModel('gemini-pro')
    response = model1.generate_content(msg)
    return response.text


# Fraud Detection
# import pickle
# import numpy as np
# from django.views.decorators.csrf import csrf_exempt

# # Load the trained model
# with open('core/fraud_detection_model.pkl', 'rb') as f:
#     model = pickle.load(f)

# # Define a function to preprocess input data and make predictions
# def predict_fraud(details):
#         features = details
#         data = [float(features[key]) for key in features]

#         # Make prediction
#         prediction = model.predict(np.array([data]))

#         # Convert prediction to human-readable format
#         if prediction[0] == "No Fraud":
#             result = "No Fraud Detected"
#         else:
#             result = "Fraud Detected"

#         # Return prediction as JSON response
#         return JsonResponse({'result': result})