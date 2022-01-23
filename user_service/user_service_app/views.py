import logging
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from user_service_app.services.service import serviceRest

logger = logging.getLogger(__name__)
_service_ = serviceRest


@csrf_exempt
def signin(request) -> HttpResponse:
    response = _service_.signin(request)
    return HttpResponse(response[1])


@csrf_exempt
def login(request) -> HttpResponse:
    response = _service_.login(request)
    resp = json.loads(response)
    if resp[0]:
        user = json.loads(resp[1])
        request.session[user['username']] = user
    return HttpResponse(response)


@csrf_exempt
def logout(request) -> HttpResponse:
    result = _service_.logout(request)
    return HttpResponse(result)


@csrf_exempt
def is_logged_in(request) -> HttpResponse:
    result = _service_.is_logged_in(request)
    return HttpResponse(result)


@csrf_exempt
def get_user_address_by_name(request) -> HttpResponse:
    user_address = _service_.get_user_address_by_name(request)
    return HttpResponse(user_address)
