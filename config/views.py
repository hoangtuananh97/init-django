from django.shortcuts import render


def healthy(request):
    return render(request, 'healthy.html')
