from django.core.handlers.wsgi import WSGIRequest
from django.http.response import JsonResponse
from sign.models import Event, Guest
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db.utils import IntegrityError
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect


def add_event(request):
    # eid = request.POST.get('eid',)
    # name = request.POST.get('name','nin')
    # address = request.POST.get('address',)
    # start_time = request.POST.get('start_time',)
    # status = request.POST.get('status',)
    eid = request.GET.get('eid','')
    name = request.GET.get('name','')
    address = request.GET.get('address','')
    start_time = request.GET.get('start_time','')
    status = request.GET.get('status','')
    request.POST

    if eid == '' or name == '' or address == '' or start_time == '' or status == '':
        return JsonResponse({'status': 10021, 'message': 'parameters error'})

    result = Event.objects.filter(id=eid)
    if result:
        return JsonResponse({'status': 10022, 'message': 'event already exist'})

    result = Event.objects.filter(name=name)
    if result:
        return JsonResponse({'status': 10023, 'message': 'event name already exist'})

    # deal with unnecesary parameters
    if status == '':
        status = 1

    try:
        Event.objects.create(name=name, status=status, address=address, start_time=start_time)
    except ValidationError as e:
        error = 'start_time format error. It must be in YYYY-MM-DD hh:mm:ss format'
        return JsonResponse({'status': 10024, 'message': error})
    return JsonResponse({'status': 200, 'message': 'Add event successfully'})

# status code:
# 10021-parameters error
# 10022-no object with eid
# 10023-no object with name
# 200-find one successfuly with eid
# 201-find one successfuly with name
def get_event_list(request):
    eid = request.GET.get('eid',)
    name = request.GET.get('name',)

    if eid== '' and name== '':
        return JsonResponse({'status': 10021, 'message': 'parameters error'})

    if eid != '':
        event = {}
        try:
            result = Event.objects.get(id=eid)
        except ObjectDoesNotExist as e:
            return JsonResponse({'status': 10022, 'message': 'query event is empty'})
        else:
            event['name'] = result.name
            event['id'] = result.id
            event['address'] = result.address
            event['start_time'] = result.start_time
            event['status'] = result.status
            return JsonResponse({'status': 201, 'message': 'get event successfully', 'data':event})

    if name != '':
        event_list = []
        results = Event.objects.filter(name__contains=name)
        if results != '':
            for result in results:
                event = {}
                event['name'] = result.name
                event['id'] = result.id
                event['address'] = result.address
                event['start_time'] = result.start_time
                event['status'] = result.status
                event_list.append(event)
            return JsonResponse({'status': 202, 'message': 'get event successfully', 'data': event_list})
        else:
            return JsonResponse({'status': 10023, 'message': 'query event is empty'})


# status code
    # 10021-parameters error
    # 10022-event not exist
    # 10023-phone repeat
    # 10024-had reach limit guests ccount
    # 10027-create fail
    # 200-add successfully

# HTTP info
#    method- Get
# Parameters
    # *eid-int
    # *phone-string
    # *realname-string
    # *create_time-date time
    # sign-boolen
    # mail-string
def add_guest(request):
    event_id = request.GET.get('eid',)
    phone = request.GET.get('phone',)
    realname = request.GET.get('realname',)

    if event_id == '' or phone == '' or realname =='':
        return JsonResponse({'status': 10021, 'message': 'parameters error'})

    event = Event.objects.get(id=event_id)
    if not event:
        return JsonResponse({'status': 10022, 'message': 'event is null'})

    guest = Guest.objects.get(phone=phone)
    if guest and guest.realname == realname:
        return JsonResponse({'status': 10023, 'message': 'phone repeat'})

    event_limit = event.limit
    sign_guest_count = len(Guest.objects.get(event_id=event_id, sign= True))
    if event_limit <= sign_guest_count:
        return JsonResponse({'status': 10024, 'message': 'had reach limit guests ccount'})

    create_time = request.Get.get('create_time',)
    sign = request.GET.get('sign',)
    mail = request.GET.get('mail',)

    try:
        Guest.objects.create(realname=realname, event_id=event_id, phone=phone, mail=mail, sign=sign, create_time=create_time)
    except IntegrityError as e:
        return JsonResponse({'status': 10027, 'message': 'parameters input incorrect, please recheck'})
    else:
        return JsonResponse({'status': 200, 'message': 'add guest successfully'})


def test(request):
    if request.method == 'POST':
        name = request.POST.get('name','')
        return JsonResponse({'status': 200, 'method': 'POST', 'name': name})
    if request.method == 'GET':
        name = request.GET.get('name', '')
        return JsonResponse({'status': 200, 'method': 'GET', 'name': name})
    return JsonResponse({'status': 200, 'method': 'nothing'})

    # name = request.Get.get('name')
    # name = request.Get.get('name',)
    # return JsonResponse({'status':200})

