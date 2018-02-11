from django.http.response import JsonResponse
from django.http.request import HttpRequest

def test(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        return JsonResponse({'status': 200, 'method1': 'POST', 'name': name})
    if request.method == 'GET':
        name = request.GET.get('name', '')
        return JsonResponse({'status': 200, 'method1': 'GET', 'name': name})
    return JsonResponse({'status': 200, 'method': 'nothing'})