from django.shortcuts import render

# Create your views here.
def tarefas_view(request):
    return render(request, 'tarefas/index.html')  