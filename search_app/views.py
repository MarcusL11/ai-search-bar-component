from django.template.response import TemplateResponse
from django.http import HttpResponse
from search_app.models import CollectableShoe
import bleach
from django.db.models import Q
from search_app.ai_assistants import AISearchAssistant
from django_ai_assistant.api.schemas import ThreadIn, ThreadMessageIn
from django_ai_assistant.helpers.use_cases import (
    create_thread,
    create_message,
)
from django_ai_assistant.models import Message


def index(request) -> HttpResponse:
    return TemplateResponse(request, "search_app/index.html")


def active_search(request) -> HttpResponse:
    search_content = request.POST.get("prompt_input", "")
    print("SEARCH CONTENT: ", search_content)

    results = []

    if not search_content:
        # if the search content is empty, return an empty response, to handle the keyup event of deleting the search content
        return HttpResponse("")  # pyright: ignore

    # Sanitize the search content using bleach
    sanitized_content = bleach.clean(
        search_content.strip(), strip=True
    )  # TODO: Add https://pypi.org/project/bleach/

    # Remove any remaining non-alphanumeric characters (except spaces)
    sanitized_content = "".join(
        char for char in sanitized_content if char.isalnum() or char.isspace()
    )
    search_content = sanitized_content

    # Filter CollectableShoes based on search_content
    results = CollectableShoe.objects.filter(  # pyright: ignore
        Q(brand__icontains=search_content)  # pyright: ignore
        | Q(model__icontains=search_content)
        | Q(collaboration_artist__icontains=search_content)
        | Q(sku_code__icontains=search_content)
        | Q(color__icontains=search_content)
        | Q(rarity__icontains=search_content)
    ).distinct()

    context = {
        "results": results,
        "search_content": search_content,
    }

    return TemplateResponse(
        request, "search_app/partials/active_search_results.html", context
    )


def ask_ai(request) -> HttpResponse:
    """This is the view function that handles the chat with AI
    feature via Django AI Assistant library."""

    user_prompt = request.POST.get("ask_ai_input")
    assistant_id = AISearchAssistant.id
    thread_data = ThreadIn(assistant_id=assistant_id)
    thread = create_thread(
        name=thread_data.name,
        user=request.user,
        request=request,
    )

    message = ThreadMessageIn(
        assistant_id=assistant_id,
        content=user_prompt,
    )
    create_message(
        assistant_id=assistant_id,
        thread=thread,
        user=request.user,
        content=message.content,
        request=request,
    )
    thread_messages = (
        Message.objects.filter(thread=thread).values("message").order_by("created_at")  # pyright: ignore
    )
    print("Thread Messages", thread_messages)

    ai_response = None
    for message in reversed(thread_messages):
        message_type = message["message"]["type"]
        print("Message Type", message_type)

        if message_type == "ai":
            message_content = message["message"]["data"]["content"]
            print("Message Content", message_content)

            ai_response = message_content
            break  # Exit the loop after finding the most recent AI message

    context = {
        "ai_response": ai_response,
        "thread_id": thread.id,
    }

    return TemplateResponse(
        request,
        "search_app/partials/ask_ai_results.html",
        context,
        status=200,
    )
