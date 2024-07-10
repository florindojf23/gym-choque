from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import UserForm
# Create your views here.
@login_required
def userlist(request):
	user = User.objects.all()
	context = {
		"userlist":user,
	}
	return render(request,"userlist.html",context)

@login_required
def create_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('userlist')  # Redirect to user list after creation
    else:
        form = UserForm()
    
    return render(request, 'create_user.html', {'form': form})

@login_required
def update_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('userlist')  # Redirect to a list or detail view
    else:
        form = UserForm(instance=user)
    
    return render(request, 'update_user.html', {'form': form})

@login_required
def delete_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    
    if request.method == 'POST':
        user.delete()
        return redirect('userlist')  # Redirect to a list or detail view
    
    return render(request, 'delete_user.html', {'user': user})