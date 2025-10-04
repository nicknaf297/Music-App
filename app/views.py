from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .forms import CreateUserForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def registerPage(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            return redirect('login')
    else:
        form = CreateUserForm()        

    context = {'form': form}
    return render(request, 'app/register.html', context)     #return page to be displayed - full path

def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username') #get from name in input in HTML
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None and user.roles == 'Artist':
            login(request, user)
            return redirect('artist_page')
        elif user is not None and user.roles == 'Listener':
            login(request, user)
            return redirect('listener_page')
        elif user is not None and user.roles == 'Admin':
            login(request, user)
            return redirect('admin_page')

    context = {}
    return render(request, 'app/newlogin.html', context) #return page to be displayed

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    if request.user.is_authenticated:
        return(redirect('/menu'))
    else:
        return render(
            request,
            'app/index.html',
            {
                'title':'Home Page',
                'year': datetime.now().year,
            }
        )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Dr. Yeoh.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'ABC System',
            'message':'This application processes ...',
            'year':datetime.now().year,
        }
    )

@login_required
def menu(request):
    check_employee = request.user.groups.filter(name='employee').exists()

    context = {
            'title':'Main Menu',
            'is_employee': check_employee,
            'year':datetime.now().year,
        }
    context['user'] = request.user

    return render(request,'app/menu.html',context)

def index(request):
       
    song = song.objects.all()
    return render(request, "index.html", {'song':song})