from django.shortcuts import render


def overview(request):
    return render(request, 'blog/post_list.html', {})
