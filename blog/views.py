from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from .models import Post
from .forms import PostForm
from django.db import IntegrityError
from django.contrib.auth import logout

# Logout view (Redirect to login page)
def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout

# Check if the user is an admin
def is_admin(user):
    return user.is_superuser

@login_required  # Requires login
@user_passes_test(is_admin)  # Requires admin access
def blog_list(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 12)  # Show 12 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/BlogList.html', {'page_obj': page_obj})

# Post detail view (Accessible to all users)
def post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'blog/PostView.html', {'post': post})

# Login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user and user.is_superuser:  # Only admin can log in
            login(request, user)
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
        else:
            messages.error(request, 'اطلاعات ورود نامعتبر است یا دسترسی محدود است.')
    return render(request, 'blog/Login.html')

# Register view (Basic users only)
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')

        if not username or not password or not confirm_password:
            messages.error(request, 'تمام فیلدها الزامی هستند.')
            return render(request, 'blog/Register.html')

        if password != confirm_password:
            messages.error(request, 'رمزهای عبور یکسان نیستند.')
            return render(request, 'blog/Register.html')

        try:
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
        except IntegrityError:
            messages.error(request, 'نام کاربری قبلاً ثبت شده است.')
            return render(request, 'blog/Register.html')

    return render(request, 'blog/Register.html')

# Create post view (Admin only)
@login_required
@user_passes_test(is_admin)
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('blog_list')
    else:
        form = PostForm()
    return render(request, 'blog/CreatePost.html', {'form': form, 'is_edit': False})

# Edit post view (Admin only)
@login_required
@user_passes_test(is_admin)
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)  # دریافت پست با ID مشخص
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog_list')
    else:
        form = PostForm(instance=post)
    # ارسال کانتکست به قالب
    return render(request, 'blog/EditPost.html', {'form': form, 'is_edit': True, 'post': post})


# Delete post view (Admin only)
@login_required
@user_passes_test(is_admin)
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        post.delete()
        return redirect('blog_list')
    return render(request, 'blog/DeletePost.html', {'post': post})
