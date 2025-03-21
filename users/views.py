from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from users.forms import UserForm, UserEditForm
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages




@login_required
def users_list(request):
    if not request.user.is_superuser:
        return redirect("dashboard")

    search = request.GET.get('search', '')
    if search:
        users_list = User.objects.filter(
            Q(username__icontains=search) |
            Q(email__icontains=search)
        ).order_by('username')
    else:
        users_list = User.objects.all().order_by('username')

    paginator = Paginator(users_list, 7)
    page_number = request.GET.get('page')
    users = paginator.get_page(page_number)

    context = {
        'users': users,
        'search': search,
    }

    return render(request, 'users/list.html', { 'users': users,'search': search, })
@login_required
def create_user(request):
    if not request.user.is_superuser:
        return redirect("dashboard")

    form=UserForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request,"User successfully created")
            return redirect("users-list")
    return render(request,"users/create.html",{"form":form})
@login_required
def edit_user(request, user_id):
    if not request.user.is_superuser:
        return redirect("dashboard")
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request,"User successfully updated")
            return redirect('users-list')
    else:
        form = UserEditForm(instance=user)
    return render(request, 'users/create.html', {'form': form})

@login_required
def delete_user(request, user_id):
    if not request.user.is_superuser:
        return redirect("dashboard")
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, "User successfully deleted")
    return redirect('users-list')

@login_required
def toggle_active_user(request, user_id):
    if not request.user.is_superuser:
        return redirect("dashboard")
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.is_active = not user.is_active
        user.save()
        status = "activated" if user.is_active else "deactivated"
        messages.success(request, f"User successfully {status}")
    return redirect('users-list')
