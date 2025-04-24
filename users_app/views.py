from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def signupView(request):
    ''' view to register new user'''
    #you dont need a form if you are using the default UserCreationForm
    # if you want to add more fields, create a custom form that inherits from UserCreationForm
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('results_app:index')  # Redirect to results_app home page
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form_key': form})
