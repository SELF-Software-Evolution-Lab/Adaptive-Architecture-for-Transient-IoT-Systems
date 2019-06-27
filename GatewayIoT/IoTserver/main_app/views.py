import json
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from .instance_matching import instance_matching


def index(request):
    return HttpResponse("<h1>Iot Server</h1>")


@csrf_exempt
def post_service(request):
    if request.method == "POST":
        received_json_data = json.loads(request.body)
        print("functional_requirement", received_json_data)
        instance_matching(received_json_data)
    return HttpResponseRedirect("/")
