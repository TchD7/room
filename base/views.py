from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,logout, authenticate
from django.contrib import messages
from .models import Room, Topic,Message
from . forms import RoomForm
from django.db.models import Q

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password  = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            #print('user est pas la ')
            messages.error(request,'User does not exist')
        user = authenticate(request, username = username,password= password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
             messages.error(request,'passeword incorrect')
    context = {'page': page}
    return render(request, 'base/login_register.html',context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):

    form = UserCreationForm()
    context = {'form':form}
    return render(request, 'base/login_register.html',context)
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(Q(topic__name__icontains = q)|
    Q(description__icontains = q)|
    Q(name__icontains = q))
    topics = Topic.objects.all()
    room_count = rooms.count()
    context = {
        'rooms': rooms,
        'topics':topics,
        'room_count':room_count,
    }
    return render(request, 'base/home.html', context)


def room(request,pk):
    room = Room.objects.get(id=pk)
    room_messages  = room.message_set.all().order_by('-created')
    #creer le message ici
    if request.method == 'POST':
        messages = Message.objects.create(
            user=request.user,
            room = room,
            body = request.POST.get('body')
        )
        return redirect('room' ,pk = room.id)
    context = { 'room': room,
    'room_messages ': room_messages 
        }
    return render(request, 'base/room.html',context)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid:
            form.save()
        return redirect('home')
    context = {
        'form': form
    }
    return render(request, 'base/form_room.html',context)

@login_required(login_url='login')
def updateroom(request,pk):
    room = Room.objects.get(id =pk)
    form = RoomForm(instance=room)
    if request.user != room.host:
        return HttpResponse('Pas permis')
    if request.method == 'POST':
        form = RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
        return redirect('home')
    context = {
        'form': form
    }
    return render(request, 'base/form_room.html',context)

@login_required(login_url='login')
def deleteRoom(request,pk):
    room = Room.objects.get(id = pk)
    if request.user != room.host:
        return HttpResponse('Pas permis')
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', { 'obj':room } )



