from django.template.response import TemplateResponse
from django.http import HttpResponse

# Create your views here.
def dashboard(request):
    return TemplateResponse(request,'index.html')
# def agent(request)
#     return HttpResponse("You're voting on question %s." %id_agent)

def test1(request):
    return TemplateResponse(request,'test.html')

def agent(request,id_agent):
    return TemplateResponse(request,'agent.html')
