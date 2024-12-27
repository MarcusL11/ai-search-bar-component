from django.template.response import TemplateResponse
from django.http import HttpResponse


def index(request) -> HttpResponse:
    return TemplateResponse(request, "search_app/index.html")
