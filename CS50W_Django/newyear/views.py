from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, "newyear/index.html", {
        "newyear": datetime.now().month == 1 and datetime.now().day == 1
    })