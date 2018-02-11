from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from sign.models import Event, Guest
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.http.response import JsonResponse

# Create your views here.


def index(request):

    return render(request, "index.html")


def login_action(request):
    if request.method == 'POST':
        userName = request.POST.get('userName', '')
        passWord = request.POST.get('password', '')
        print(userName)
        user = auth.authenticate(username=userName, password=passWord)
        if user is not None:
            auth.login(request, user)
            request.session['usr11'] = userName
            response = HttpResponseRedirect('/login_success/')
            return response

        else:
            return render(request, 'index.html', {'error': 'userName or password incorrect'})


@login_required
def login_success(request):
    #cookies
    #usrName = request.COOKIES.get('user', '')

    #session
    usrName = request.session.get('usr11', '')

    #get all objects from event_list
    event_list = Event.objects.all()
    return render(request, 'event_manage.html', {'userName': usrName, 'event_list': event_list})


@login_required
def guest_manage(request):
    usrName = request.session.get('usr11', '')

    #get all objects from event_list
    guest_list = Guest.objects.all()
    paginator = Paginator(guest_list,2)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)

    return render(request, 'guest_manage.html', {'userName': usrName, 'guest_list': contacts})


# search event name
@login_required
def search_name(request):
    usrName = request.session.get('usr11', '')
    search_name = request.GET.get('name',)
    event_list = Event.objects.filter(name__contains=search_name)
    return render(request, 'event_manage.html', {'userName': usrName, 'event_list': event_list})


# search event name
@login_required
def search_guest(request):
    usrName = request.session.get('usr11', '')
    search_guest = request.GET.get('name',)
    guest_list = Guest.objects.filter(realname__contains=search_guest)

    return render(request, 'guest_manage.html', {'userName': usrName, 'guest_list': guest_list})


#sign function
@login_required
def sign_index(request, eid):
    usrName = request.session.get('usr11', '')
    event = get_object_or_404(Event, id=eid)
    return render(request, 'sign_index.html', {'event': event, 'userName': usrName})


#sign action
@login_required
def sign_index_action(request, eid):
    usrName = request.session.get('usr11', '')
    event = get_object_or_404(Event, id=eid)
    phone = request.POST.get('phone',)
    print(phone)

    #check whether phone exist
    result = Guest.objects.filter(phone=phone)
    if not result:
        return render(request, 'sign_index.html', {'event': event, 'hint': 'phone error','userName': usrName})

    #check whether the guest join the event
    result = Guest.objects.filter(phone=phone, event_id=eid)
    if not result:
        return render(request, 'sign_index.html', {'event': event, 'hint': 'phone or event error','userName': usrName})

    # check whether the guest join the event
    result = Guest.objects.get(phone=phone, event_id=eid)
    if result.sign:
        return render(request, 'sign_index.html', {'event': event, 'hint': 'user has been signed','userName': usrName})
    else:
        Guest.objects.filter(phone=phone, event_id=eid).update(sign='1')
        return render(request, 'sign_index.html', {'event': event, 'hint': 'sign successfully', 'guest': result,'userName': usrName})


#logout function
@login_required
def logout(request):
    auth.logout(request)
    response = HttpResponseRedirect('/index/')
    return response


def test(request):
    if request.method == 'POST':
        name = request.GET.get('name', '')
        print(request.GET.get('name'))
        return JsonResponse({'status': 200, 'method1': 'POST', 'name': name})
    if request.method == 'GET':
        name = request.GET.get('name', '')
        print(request.content_params.get('name'))
        return JsonResponse({'status': 200, 'method1': 'GET', 'name': name})
    return JsonResponse({'status': 200, 'method': 'nothing'})

