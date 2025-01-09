from django.shortcuts import render
from django.views import View

class AuthView(View):
    def get(self, request):
        return render(request, 'auth.html')