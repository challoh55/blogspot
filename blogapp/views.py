from django.shortcuts import redirect, render, get_object_or_404
from .models import NewPost, User, Comment
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.urls import reverse




# Create your views here.

#home
def homepage(request):
    allposts = NewPost.objects.all().order_by('-created_at')

    post_counts = NewPost.newpost_count() # to display blog most blogged based on function in newpost model
    bloggers = User.objects.all().exclude(is_superuser=True)



    page = Paginator(allposts, 10)
    page_list = request.GET.get('page')
    page = page.get_page(page_list)

    context = {'page':page, 'post_counts':post_counts, 'bloggers':bloggers}

    return render(request, 'blogapp/home.html', context)



def register(request):

    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        image = request.FILES.get('image')
        fname =request.POST.get('fname')
        lname =request.POST.get('lname')
        dob =request.POST.get('dob')
        phonenumber = request.POST.get('phonenumber')


        if User.objects.filter(email=email).exists():
            messages.warning(request, 'Email already exists')
            return redirect('register_user')
        
        if User.objects.filter(username=username).exists():
            messages.warning(request, 'User already exists')
            return redirect('register_user')

        new_user = User.objects.create_user(email=email, username=username, password=password, image=image, first_name=fname, last_name=lname, dob=dob, phonenumber=phonenumber)
        new_user.save()

        messages.success(request, 'Your account has been successfully created. Proceed to login')
        return redirect('login_user')

    return render(request, 'blogapp/register.html')



def Login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Welcome!!! Read and add blogs')
            return redirect('user_homepage')
        else:
            messages.warning(request, 'Invalid Credentials. Please enter the correct username and password!!')
    

    return render(request, 'blogapp/login.html')



def Logout(request):
    logout(request)
    return redirect('home_page')


def update_profile(request):
    users = request.user

    if request.method == 'POST':
        # users.email = request.GET.get('email')
        users.username = request.POST.get('username')
        if 'image' in request.FILES:
            users.image = request.FILES['image']

        messages.success(request, 'Your profile has been successfully updated')
        
        users.save()
        return redirect('user_homepage')
    
    context ={'users':users}
    return render(request, 'blogapp/updateprofile.html', context)



@login_required(login_url='login_user') 
def user_homepage(request):
    username = request.user
    allposts = NewPost.objects.all().order_by('-created_at')
    bloggers = User.objects.all().exclude(is_superuser=True)


    post_counts = NewPost.newpost_count() # to display blog most blogged based on function in newpost model
    most_comments = NewPost.most_comments_count()

    page = Paginator(allposts, 5)
    page_list = request.GET.get('page')
    page = page.get_page(page_list)

    context = {'page':page, 'username':username, 'post_counts':post_counts, 'most_comments':most_comments,'bloggers':bloggers}

    return render(request, 'blogapp/userhomepage.html', context)



@login_required(login_url='login_user') 
def add_new_post(request):
    user = request.user
    if request.method == 'POST':
        title = request.POST.get('title').capitalize()
        content = request.POST.get('content').capitalize()
        image = request.FILES.get('image')
        
        new_post = NewPost(user=user, title=title, content=content, image=image)
        new_post.save()

        return redirect('add_new_post')

    myposts = NewPost.objects.filter(user=user).order_by('-created_at')

    context = {'myposts':myposts, 'username':user}
    return render(request, 'blogapp/addnewpost.html', context)




@login_required(login_url='login_user') 
def delete_post(request):
    post_id = request.GET.get('id')
    post = NewPost.objects.get(id=post_id)
    post.delete()

    return redirect('add_new_post')



@login_required(login_url='login_user') 
def update_post(request):
    username = request.user

    post_id = request.GET.get('id')
    post = NewPost.objects.get(id=post_id)

    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')

        post.save()
        return redirect('add_new_post')
    context = {'username':username, 'post':post}
    return render(request, 'blogapp/updatepost.html', context)




@login_required(login_url='login_user') 
def view_post_details(request):
    username = request.user
    post_id = request.GET.get('id')
    post = NewPost.objects.get(id=post_id)

    if request.method == 'POST':
        commment = request.POST.get('comment')
        comments = Comment(user=username, post= post, content=commment)
        comments.save()

    total_likes = post.total_likes()
    liked_users = post.likes.all()

    related_post = NewPost.objects.filter(user=username)

    context={'post':post, 'username':username, 'related_post':related_post, 'total_likes':total_likes, 'liked_users':liked_users}
    return render(request, 'blogapp/viewpostdetails.html', context)


@login_required(login_url='login_user') 
def all_posts_for_topic(request):
    user = request.user
    title = request.GET.get('title')

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'like':
            post_id = request.POST.get('post_id')
            post = NewPost.objects.get(id=post_id)
            post.likes.add(user)
            post.save()

        elif action == 'comment':
            post_id = request.POST.get('post_id')
            comment_content = request.POST.get('comment')
            post = NewPost.objects.get(id=post_id)
            comment = Comment(user=user, post=post, content=comment_content)
            comment.save()

    related_posts = NewPost.objects.filter(user=user)
    all_posts = NewPost.objects.filter(title=title).order_by('-created_at')
    context = {'all_posts': all_posts, 'title': title, 'related_posts': related_posts}
    return render(request, 'blogapp/allpostsfortopic.html', context)




@login_required(login_url='login_user') 
def Posts_by_user(request):
    username = request.user
    user_id = request.GET.get('id')
    user1 = User.objects.get(id=user_id)

    if request.method == 'POST':
        comment_content = request.POST.get('comment')
        post_id = request.POST.get('post_id')  # Assuming you have a hidden input for post_id in your form
        post = NewPost.objects.get(id=post_id)
        user = request.user

        # Create and save the comment
        comment = Comment(user=user, post=post, content=comment_content)
        comment.save()

    related_post = NewPost.objects.filter(user=username)
    posts = NewPost.objects.filter(user=user1)

    context = {'posts':posts, 'user2':user1, 'username':username, 'related_post':related_post}
    return render(request, 'blogapp/postsbyuser.html', context)


def Like_post(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post = get_object_or_404(NewPost, id=post_id)
        post.likes.add(request.user)
    return HttpResponseRedirect(reverse('view_post_details') + f'?id={post_id}')
