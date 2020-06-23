from django.http import JsonResponse

from blueking.component.shortcuts import get_client_by_request
from blueapps.account.decorators import login_exempt
# Create your views here.


@login_exempt
def test_api(request):
    if request.COOKIES and request.COOKIES.get('bk_token'):
        bk_token = request.COOKIES['bk_token']
        params = {
            'bk_token': bk_token
        }
        result = get_client_by_request(request).bk_login.get_user(params)
        username = result['data']['bk_username']
    else:
        username = ''
    return JsonResponse({'result': True, 'data': username})
