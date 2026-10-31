from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from .models import Profile, Post, Comment, Follow


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def home(request):
    # Creating a new post
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            Post.objects.create(author=request.user, content=content)
        return redirect('home')

    posts = Post.objects.all().order_by('-created')

    # IDs of the people I follow
    following_ids = list(
        Follow.objects.filter(follower=request.user).values_list('following_id', flat=True)
    )

    # "Following" tab: my posts + posts from people I follow
       # "Following" tab: only posts from people I follow
    if request.GET.get('filter') == 'following':
        posts = posts.filter(author_id__in=following_ids)

    # Everyone except me, so I can follow them from the home page
    people = User.objects.exclude(id=request.user.id)

    return render(request, 'home.html', {
        'posts': posts,
        'people': people,
        'following_ids': following_ids,
    })

@login_required
@require_POST
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)   # already liked -> unlike
    else:
        post.likes.add(request.user)
    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required
@require_POST
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    text = request.POST.get('text', '').strip()
    if text:
        Comment.objects.create(post=post, author=request.user, text=text)
    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required
@require_POST
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)  # only the author can delete
    post.delete()
    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required
def profile(request, username):
    owner = get_object_or_404(User, username=username)
    profile, created = Profile.objects.get_or_create(user=owner)
    context = {
        'owner': owner,
        'profile': profile,
        'posts': Post.objects.filter(author=owner).order_by('-created'),
        'followers_count': Follow.objects.filter(following=owner).count(),
        'following_count': Follow.objects.filter(follower=owner).count(),
        'is_following': Follow.objects.filter(follower=request.user, following=owner).exists(),
    }
    return render(request, 'profile.html', context)


@login_required
@require_POST
def follow_user(request, username):
    target = get_object_or_404(User, username=username)
    if target != request.user:
        existing = Follow.objects.filter(follower=request.user, following=target)
        if existing.exists():
            existing.delete()    # already following -> unfollow
        else:
            Follow.objects.create(follower=request.user, following=target)
    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        profile.bio = request.POST.get('bio', '').strip()
        profile.save()
        return redirect('profile', username=request.user.username)
    return render(request, 'edit_profile.html', {'profile': profile})

@login_required
def follow_list(request, username, kind):
    owner = get_object_or_404(User, username=username)
    if kind == 'followers':
        rows = Follow.objects.filter(following=owner).select_related('follower')
        users = [row.follower for row in rows]
    else:
        rows = Follow.objects.filter(follower=owner).select_related('following')
        users = [row.following for row in rows]
    return render(request, 'follow_list.html', {'owner': owner, 'kind': kind, 'users': users})