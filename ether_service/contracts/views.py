import logging

from django.core.exceptions import BadRequest
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from contracts.services.service import contractService

_service_ = contractService
logger = logging.getLogger(__name__)


@csrf_exempt
def deploy(request) -> HttpResponse:
    try:
        _response_ = _service_.deploy(request)
    except BaseException as exc:
        return HttpResponseBadRequest(reason=exc.args)
    return HttpResponse(_response_)
