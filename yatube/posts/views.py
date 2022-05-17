from django.shortcuts import render

from .models import Post


def index(request):
    latest = Post.objects.order_by("-pub_date")[:11]
    context = {"posts": latest}
    response = render(request, "index.html", context)
    return response