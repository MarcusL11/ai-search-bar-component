from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("htmx/active-search/", views.active_search, name="active_search"),
    path("htmx/ask-ai/", views.ask_ai, name="ask_ai"),
    path("htmx/ask-ai-cont/<int:thread_id>/", views.ask_ai_cont, name="ask_ai_cont"),
]
