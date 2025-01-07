from django.shortcuts import render
from django.views import View

class MainFView(View):
    def get(self, request):
        return render(request, 'main.html')
