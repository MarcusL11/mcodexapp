from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Subscriber, Tag, TableOfContent, BlogPost
from .forms import CreateUserForm, UserLoginForm, SubscriberForm, UpdateProfilePicForm
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404
from django.shortcuts import get_object_or_404

# Create your views here.
def home(request):
    blogposts = BlogPost.objects.all().order_by('-publish_date')
    latest_blog_post = BlogPost.objects.order_by('-publish_date').first()
    latest_blog_intro = latest_blog_post.intro[:250]
    tags = Tag.objects.values('name').distinct().order_by('name')

    context = {
        'blogposts': blogposts,
        'latest_blog_post': latest_blog_post,
        'latest_blog_intro': latest_blog_intro,
        'tags': tags,
    }

    return render(request, 'blogapp/index.html', context=context)

def blogpage(request, slug):
    try:
        post = BlogPost.objects.get(slug=slug)
        tags = Tag.objects.filter(blogpost=post.id).order_by('name')
        toc = TableOfContent.objects.filter(blogpost=post.id)
       
        context = {
            'post': post,
            'tags': tags,
            'toc': toc,
        }
    except BlogPost.DoesNotExist:
        raise Http404("Blog does not exist")
    return render(request, 'blogapp/blogpage.html', context=context)

def categories(request, tag_id=None):
    if tag_id == "all":
        blog_categories = BlogPost.objects.order_by('-publish_date')
        tags =Tag.objects.values('name').distinct().order_by('name')

        context = {
            'blog_categories': blog_categories,
            'tags': tags,
            'tag': 'all',  
        }


        return render(request, 'blogapp/categories.html', context=context)
    else:
        try:
            tag = get_object_or_404(Tag, name=tag_id)
            blog_categories = BlogPost.objects.filter(tags=tag).order_by('-publish_date')
            tags = Tag.objects.filter(blogpost__in=blog_categories).order_by('name').distinct()
            context = {
                'blog_categories': blog_categories,
                'tags': tags,
                'tag': tag,
            }
            return render(request, 'blogapp/categories.html', context)
        except Tag.DoesNotExist:
            raise Http404("Category does not exist")            
    



def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                form.cleaned_data['username'],
                form.cleaned_data['email'],
                form.cleaned_data['password1']
            )
            subscriber = Subscriber.objects.create(
                user=user,
            )
        
            subscriber.save()

            return redirect("login")
        else:
            return render(request, 'blogapp/register.html', {'form': form})

    return render(request, 'blogapp/register.html', {'form': form})

def user_login(request):
    form = UserLoginForm()

    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("profile")
            else:
                form.add_error(None, "Invalid username or password")

    return render(request, 'blogapp/login.html', {'form': form})

def user_logout(request):  
    logout(request)  
    return redirect("home")

@login_required(login_url="login")
def profile(request):
    subscriber = Subscriber.objects.get(user=request.user)
    form = SubscriberForm(instance=subscriber)
    form2 = UpdateProfilePicForm(instance=subscriber)
    subscriber_status = subscriber.subscribe

    if request.method == "POST":
    
        form = SubscriberForm(request.POST, instance=subscriber)
        form2 = UpdateProfilePicForm(request.POST, request.FILES, instance=subscriber)
    
        if form.is_valid():
            form.save()
            messages.success(request, "Profile Updated!")
            return redirect("profile")
        
        if form2.is_valid():
            form.save()
            messages.success(request, "Profile Picture Updated!")
            return redirect("profile")
        
    context = {
        'form': form,
        'form2': form2,
        'subscriber_status': subscriber_status,
        'subscriber': subscriber,
    }
    return render(request, 'blogapp/profile.html', context=context)

def update_profile_pic(request):
    subscriber = Subscriber.objects.get(user=request.user)

    form = UpdateProfilePicForm(instance=subscriber)

    if request.method == "POST":
        form = UpdateProfilePicForm(request.POST, request.FILES, instance=subscriber)

        if form.is_valid():
            form.save()
            messages.success(request, "Profile Picture Updated!")
            return redirect("profile")

    return render(request, 'blogapp/update_profile_pic.html', {'form': form})
