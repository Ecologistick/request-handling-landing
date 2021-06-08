from collections import Counter
from django.shortcuts import render

# Для отладки механизма ab-тестирования используйте эти счетчики
# в качестве хранилища количества показов и количества переходов.
# но помните, что в реальных проектах так не стоит делать
# так как при перезапуске приложения они обнулятся
counter_show = Counter()
counter_click = Counter()


def index(request):
    req = request.GET.get("from-landing")
    counter_click[req] += 1
    return render(request, 'index.html')


def landing(request):
    original_land = "landing.html"
    test_land = "landing_alternate.html"
    req = request.GET.get("ab_test_arg", "original")
    if req == "test":
        counter_show[req] += 1
        return render(request, test_land)
    else:
        counter_show[req] += 1
        return render(request, original_land)


def stats(request):
    return render(request, 'stats.html', context={
        'test_conversion': counter_click["test"] / counter_show["test"],
        'original_conversion': counter_click["original"] / counter_show["original"],
    })
