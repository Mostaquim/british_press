from django.shortcuts import render

# Create your views here.


def test_form(request):
    return render(request, 'form/test.html', {})
