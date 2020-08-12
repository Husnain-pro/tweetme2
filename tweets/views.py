import random

from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render

from tweets.models import Tweet

from .forms import TweetForm


# Create your views here.
def home_view(request):
    return render(request, "pages/home.html", context={}, status=200)


def tweet_list_view(request, *args, **kwargs):
    qs = Tweet.objects.all()
    tweet_list = [{"id": x.id, "content": x.content,
                   "likes": random.randint(0, 12)} for x in qs]
    data = {
        "respose": tweet_list
    }
    return JsonResponse(data)


def tweet_create_view(request, *args, **kwargs):
    form = TweetForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        form = TweetForm()
    return render(request, 'components/form.html', context={"form": form})


def tweet_detail_view(request, tweet_id, *args, **kwargs):
    """
    REST API VIEW
    Consume by JavaScript or Swift/Java/iOS/Andriod
    return json data
    """
    data = {
        "id": tweet_id,
    }
    status = 200
    try:
        obj = Tweet.objects.get(id=tweet_id)
        data['content'] = obj.content
    except:
        data['message'] = "Not found"
        status = 404
    # json.dumps content_type='application/json'
    return JsonResponse(data, status=status)
